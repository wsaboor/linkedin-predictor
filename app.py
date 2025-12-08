import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import plotly.express as px

# -------- PAGE CONFIG --------
st.set_page_config(page_title="LinkedIn Usage Prediction Dashboard", layout="wide")

# -------- LOAD & CLEAN DATA --------
df = pd.read_csv("social_media_usage.csv")

def clean_sm(x):
    return np.where(x == 1, 1, 0)

df = df.copy()
df["sm_li"] = clean_sm(df["web1h"])
df["income"] = df["income"].apply(lambda x: x if 1 <= x <= 9 else np.nan)
df["education"] = df["educ2"].apply(lambda x: x if 1 <= x <= 8 else np.nan)
df["parent"] = clean_sm(df["par"])
df["married"] = clean_sm(df["marital"])
df["female"] = np.where(df["gender"] == 2, 1, 0)
df["age"] = df["age"].apply(lambda x: x if 18 <= x <= 98 else np.nan)

df = df[["sm_li", "income", "education", "married", "parent", "female", "age"]].dropna()

# -------- LABEL DICTIONARIES --------
income_labels = {
    1:"< $10K",2:"$10K–$20K",3:"$20K–$30K",4:"$30K–$40K",
    5:"$40K–$50K",6:"$50K–$75K",7:"$75K–$100K",8:"$100K–$150K",9:">$150K"
}

education_labels = {
    1:"Less than high school",2:"High school incomplete",3:"High school diploma",
    4:"Some college",5:"Associate degree",6:"Bachelor’s degree",
    7:"Some graduate study",8:"Postgraduate degree"
}

# -------- TRAIN MODEL --------
features = df[["income", "education", "married", "parent", "female", "age"]]
target = df["sm_li"]
model = LogisticRegression(class_weight="balanced", max_iter=1000)
model.fit(features, target)

st.sidebar.markdown(
    """
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" 
         width="40" style="margin-bottom:-10px;">
    """, 
    unsafe_allow_html=True
)

st.sidebar.title("User Profile Selection")

# -------- SIDEBAR UI INPUT --------

income_label = st.sidebar.selectbox("Household Income", list(income_labels.values()))
education_label = st.sidebar.selectbox("Education Completed", list(education_labels.values()))
parent_label = st.sidebar.selectbox("Parent (Child under 18)", ["Yes", "No"])
married_label = st.sidebar.selectbox("Marital Status", ["No", "Married"])
gender = st.sidebar.radio("Gender", ["Male", "Female"])
age = st.sidebar.slider("Age", 18, 98, 30)

predict_button = st.sidebar.button("🔍 Predict LinkedIn Usage", use_container_width=True)

# Convert labels to numeric values
income = [k for k,v in income_labels.items() if v == income_label][0]
education = [k for k,v in education_labels.items() if v == education_label][0]
parent_num = 1 if parent_label == "Yes" else 0
married_num = 1 if married_label == "Married" else 0
gender_num = 1 if gender == "Female" else 0

# -------- MAIN TITLE --------
st.markdown("<h1 style='text-align:center;'> LinkedIn Usage Prediction Dashboard</h1>", unsafe_allow_html=True)
st.write("")

# -------- TABS --------
tab1, tab2, tab3 = st.tabs(["Prediction", "Probability Curve", "Comparison Dashboard"])

# TAB 1 — PREDICTION + 3D VISUALIZATION
with tab1:
    st.subheader("🧠 LinkedIn Usage Prediction")

    if predict_button:
        user_input = np.array([[income, education, married_num, parent_num, gender_num, age]])
        prediction = model.predict(user_input)[0]
        probability = model.predict_proba(user_input)[0][1]

        if prediction == 1:
            st.success(f"✔ This person IS likely a LinkedIn User (Probability: {probability*100:.2f}%)")
        else:
            st.error(f"❌ This person is NOT likely a LinkedIn User (Probability: {probability*100:.2f}%)")

        # 3D Chart
        fig = px.scatter_3d(
            df,
            x="age",
            y="income",
            z="education",
            color="sm_li",
            opacity=0.7,
            title="3D Visualization — Age × Income × Education",
            labels={"sm_li": "LinkedIn User"}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Click **Predict LinkedIn Usage** on the left sidebar to see results.")

# TAB 2 — AGE PROB CURVE
with tab2:
    st.subheader("Age-Based Probability Curve")

    age_range = np.arange(18,98)
    data = np.column_stack([np.repeat(income, len(age_range)),
                            np.repeat(education, len(age_range)),
                            np.repeat(married_num, len(age_range)),
                            np.repeat(parent_num, len(age_range)),
                            np.repeat(gender_num, len(age_range)),
                            age_range])
    prob_curve = model.predict_proba(data)[:,1]

    fig_age = px.line(x=age_range, y=prob_curve,
                      labels={"x":"Age","y":"Probability"},
                      title="Probability of Using LinkedIn as Age Increases")
    st.plotly_chart(fig_age, use_container_width=True)

with tab3:
    st.markdown("## 📊 Advanced LinkedIn Usage Demographic Explorer")

    st.write("Interact with demographics to uncover usage insights and patterns.")

    compare_feature = st.selectbox(
        "Select Demographic to Compare",
        ["Income", "Education", "Gender", "Parent", "Marital Status"],
        index=0
    )

    # Compute group statistics dynamically
    if compare_feature == "Gender":
        df_group = df.groupby("female")["sm_li"].mean().reset_index()
        df_group["female"] = df_group["female"].map({0: "Male", 1: "Female"})
        x_col = "female"
    elif compare_feature == "Parent":
        df_group = df.groupby("parent")["sm_li"].mean().reset_index()
        df_group["parent"] = df_group["parent"].map({0: "No", 1: "Yes"})
        x_col = "parent"
    elif compare_feature == "Marital Status":
        df_group = df.groupby("married")["sm_li"].mean().reset_index()
        df_group["married"] = df_group["married"].map({0: "Not Married", 1: "Married"})
        x_col = "married"
    elif compare_feature == "Education":
        df_group = df.groupby("education")["sm_li"].mean().reset_index()
        df_group["education"] = df_group["education"].map(education_labels)
        x_col = "education"
    else:
        df_group = df.groupby("income")["sm_li"].mean().reset_index()
        df_group["income"] = df_group["income"].map(income_labels)
        x_col = "income"

    # KPI Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Highest Using Group", df_group.loc[df_group['sm_li'].idxmax()][x_col])
    col2.metric("Lowest Using Group", df_group.loc[df_group['sm_li'].idxmin()][x_col])
    col3.metric("Difference", f"{(df_group['sm_li'].max() - df_group['sm_li'].min())*100:.1f}%")

    # Interactive Bar Graph
    fig2 = px.bar(
        df_group,
        x=x_col,
        y="sm_li",
        color="sm_li",
        color_continuous_scale="Blues",
        title=f"LinkedIn Usage by {compare_feature}",
        labels={"sm_li": "LinkedIn Probability"},
        height=450
    )
    fig2.update_layout(xaxis_title=compare_feature, yaxis_title="Probability", showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

    # Persona Generator
    st.markdown("### 🧠 Persona Insight Generator")
    selected_group = st.selectbox("Select a Group:", df_group[x_col].tolist())

    persona = ""
    if selected_group in ["Female"]:
        persona = "The Career Builder — Highly active on professional platforms, networking-oriented."
    elif selected_group in ["Male"]:
        persona = "The Opportunity Seeker — Uses LinkedIn for job transitions and skill exposure."
    elif selected_group in ["$150K+"] or "Postgraduate":
        persona = "The Executive — Uses LinkedIn as a visibility and leadership tool."
    elif selected_group in ["Less than high school"]:
        persona = "The Offline Networker — Relies more on community and traditional networking."
    else:
        persona = "The Digital Explorer — Engages when opportunities align, still forming digital habits."

    st.info(f"**{selected_group}:** {persona}")

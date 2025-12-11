**EGRA Data Transformation Pipeline – README Overview**

This module implements a transparent, reproducible data-cleaning pipeline for EGRA (Early Grade Reading Assessment) data collected via SurveyCTO. It standardizes key fields, flags inconsistencies, and produces decision-ready data for analysis while keeping a clear audit trail of all corrections.

**How to Run the Pipeline**
From the project directory, run:
python transform_egra.py \
  --input "Dataset for Pipeline Exercise - for candidate.xlsx" \
  --output "cleaned.csv" \
  --error-report "errors.csv"

**What the Pipeline Produces**
1. Cleaned Dataset (cleaned.csv)
A standardized dataset where:
- Invalid or inconsistent values are corrected or set to missing
- Impossible records (e.g., missing or non-numeric IDs) are excluded
- Dates are converted to YYYY-MM-DD
- All variables are coerced to expected ranges and formats
- Logical contradictions (e.g., no previous schooling + completed Grade 3) are resolved

2. Error Report (errors.csv)
A structured audit log that records:
- Row index and student ID
- Variable involved
- Raw value that triggered the issue
- Error type (invalid format, out of range, logical inconsistency)
- Action taken (set_to_missing, corrected, flag_only, or removed)
- This allows full transparency and supports improvements in field data collection.

**What the Script Does**
The pipeline applies a sequence of transparent cleaning steps:
- ID validation – Required for each record; missing IDs removed
- Date parsing – Multiple input formats accepted; weekend dates flagged
- Time validation – Ensures start_time precedes end_time
- Assent normalization – Converts to yes or no
- Age validation – Ensures plausible range (8–14)
- Schooling checks – Standardizes grade fields and flags contradictions
- Score validation – Ensures LSID/ORF scores fall within expected bounds
*All issues are logged, but only critical structural failures result in row removal.*

**Using the Pipeline on New Datasets**
Just run:
- python transform_egra.py --input "new_data.xlsx"
*As long as the dataset follows the same schema (13 variables), the pipeline will clean it automatically and produce both outputs.*

**Limitations**
- No statistical imputation
- No machine-learning-based corrections
- Leaves ambiguous cases to analyst judgment (but logs them clearly)
  
**Summary**
This pipeline balances rigour, simplicity, and traceability and prioritizes:
  - Clean, reliable datasets
  - Transparent handling of all issues
  - Reproducible processes
  - Field-ready feedback loops

**EGRA Data Transformation Pipeline – README Overview**

This module provides a transparent, reproducible, and program-ready pipeline for cleaning Early Grade Reading Assessment (EGRA) data collected through SurveyCTO tablets. 
The primary purpose is to ensure that data used by program and research teams is accurate, consistent, and decision-ready, while maintaining a clear audit trail for all transformations applied.

**The module produces two deliverables:**

1. Cleaned Dataset(.csv)
A standardized dataset where:
- Invalid or inconsistent values are corrected or set to missing
- Impossible records (e.g., missing or non-numeric IDs) are removed
- Dates are harmonized into a single YYYY-MM-DD format
- All variables adhere to expected ranges and formats

2. Error Report(.csv)
A structured audit log documenting:
- Which record was affected (row index and ID)
- The variable where the issue occurred
- The type of issue detected (invalid format, logical inconsistency, out of range, etc.)
- The action taken (set to missing, corrected, flagged, or removed)
- Notes explaining context where applicable
- The error report enables teams to monitor data quality, identify recurrent issues, and improve field protocols or digital data collection tools.

**System Requirements**
- Python 3.9+

**Packages:**
- pandas
- numpy

**Install dependencies:**
- pip install -r requirements.txt

**How to Run the Pipeline**
- Run the module from the project directory:
- python transform_egra.py \
  --input "Dataset for Pipeline Exercise - for candidate.xlsx" \
  --output "cleaned.csv" \
  --error-report "error.csv"

**Parameters**
  - --input	Path to raw .xlsx or .csv EGRA dataset
  - --output	Destination path for cleaned dataset
  - --error-report	Destination path for error log

**What the Pipeline Does**
1. Validates the dataset structure - Ensures all expected variables are present and properly named.
2. Cleans and standardizes key fields:
    - ID – Non-numeric or missing IDs are flagged; missing IDs are removed from the cleaned dataset
    - Date of interview – Accepts multiple formats, converts to YYYY - MM - DD format, rejects weekend dates
    - Times – Validates start–end sequence, flags inconsistencies
    - Assent – Normalizes to yes/no
    - Age – Enforces allowable range (8–14)
    - Schooling variables – Standardizes enrollment responses and grade formatting; identifies contradictions
    - Scores (LSID/ORF) – Ensures values fall within expected operational ranges
    
3. Logs every issue transparently
    - row_index: The numeric row position in the dataset where the issue occurred. The idea is to enable quick lookup in the raw file.
    - id: The student ID associated with the record. If the ID itself is the issue (e.g., "SKIPPED"), it appears as such.
    - value: The raw value as it appeared in the dataset before cleaning.
        eg: "SKIPPED", "25:61" (invalid time), "14152025" (invalid date)
    - error_type: Describes the category of problem detected.
        eg:invalid_format, invalid_value, logical_inconsistency, inconsistent_time, out_of_range, missing_value
    - action: Shows what the pipeline decided to do about the issue.
        eg: set_to_missing, corrected (e.g., turning 3 into Grade 3), flag_only (issue noted but kept in cleaned data), removed_row (for missing IDs)
    - notes: Gives additional explanation to support interpretation.

4. Produces clean, analysis-ready data
    - All structural errors (e.g., missing ID) are excluded from the cleaned dataset
    - All other issues are corrected, set to missing, or flagged
    - Cleaned data is ready for integration into dashboards, statistical analysis, or programme reporting
  
**Review the error report:**
  - Share with field and programme teams
  - Identify training needs or Kobo/SurveyCTO form improvements
  - Strengthen future data collection efforts

**Using the Pipeline on Future Datasets**
The module is reusable with any EGRA dataset, following the same structure and steps:
  1. Place the new dataset in the working directory.
  2. Run: *python transform_egra.py --input "new_data.xlsx"*
  3. Share the error report with project or field teams to strengthen future data collection practices.

**Limitations & Future Enhancements**
This module intentionally does not:
  - Impute or infer missing values.
  - Apply statistical or machine–learning–based corrections
  - Resolve ambiguous logic programmatically

**Potential enhancements:**
  - More extensive cross-variable logic (e.g., age–grade alignment)
  - Automated dashboards based on error logs
  - Integration with a cloud orchestrator (Airflow, Prefect)
  - Automated ingestion from SurveyCTO via API

**Summary**
This pipeline balances rigour, simplicity, and traceability and prioritizes:
  - Clean, reliable datasets
  - Transparent handling of all issues
  - Reproducible processes
  - Field-ready feedback loops

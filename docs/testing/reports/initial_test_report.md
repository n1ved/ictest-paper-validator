# Testing Report

**Date:** 2026-04-25
**Scope:** Functional testing of the `ictest-format-checker` application across all execution methods and validation of the existing test dataset.

---

## 1. Batch Folder Validation Testing

The batch processing script (`folder_validate.py`) was executed against both the `papers/valid` and `papers/invalid` directories to verify its ability to process multiple files, generate markdown reports, and render annotated PDFs.

- **Command executed:** `python folder_validate.py papers/valid` & `python folder_validate.py papers/invalid`
- **Result:** **PASS**
- **Observations:** 
  - The script successfully created `logs/` and `output/` subdirectories in both target folders.
  - Markdown reports (`*_report.md`) were correctly generated summarizing the formatting issues.
  - Annotated PDFs (`*_validated.pdf`) were successfully rendered containing visual red text highlights corresponding to the detected span errors.

---

## 2. API Endpoint Testing

The Flask web server was started, and a direct `POST` request was made to the `/validate` endpoint using `curl` to simulate an external integration.

- **Command executed:** `curl -X POST -F "file=@papers/valid/2V.pdf" http://127.0.0.1:5000/validate`
- **Result:** **PASS**
- **Observations:** 
  - The endpoint responded with a correct HTTP 200 status code.
  - The response payload was properly structured JSON containing `"status": "success"` and `"validation": "pass"`.
  - The `"logs"` array accurately populated the informative logs (such as the extracted author emails).

---

## 3. Test Data Validity Analysis

The user requested a manual evaluation of the test dataset to ensure the categorization into `valid` and `invalid` folders was logically sound according to the system's rules.

- **`papers/valid` Directory:** 
  - **Result:** **PASS**
  - **Analysis:** Papers in this folder (e.g., `2.pdf`, `2V.pdf`, `4V.pdf`) correctly passed *all* validation checks. The generated reports confirm a clean bill of health with zero formatting errors detected.

- **`papers/invalid` Directory:**
  - **Result:** **PASS**
  - **Analysis:** Papers in this folder correctly triggered validation failures for legitimate reasons defined in the `app/configs/guidelines.py`. Examples verified:
    - **`1V.pdf`:** Failed due to a page count violation (5 pages, where the guidelines specify `MIN_PAGES = 6`) and table formatting mismatches.
    - **`6V.pdf`:** Failed due to 4 occurrences of "Heading format mismatch", indicating Level 1 Headings were incorrectly styled.
    - **`7V.pdf`:** Failed on multiple fronts, crucially lacking the required PDF eXpress metadata certification, alongside table and reference numbering errors.

### Conclusion on Test Data
The categorization of the test data is **highly accurate**. The "invalid" papers are not arbitrarily failing due to software crashes, but rather they are legitimately failing specific, granular formatting rules expected by the conference guidelines.

---

## Final Verdict
The system is fully operational across Batch Processing and API endpoints. The underlying validation logic correctly identifies edge-case formatting issues, and the test data reliably exercises both the passing and failing pathways of the application.

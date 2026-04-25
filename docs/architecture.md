# Architecture Overview

The ICTEST Format Checker is a modular application built with Flask. Its primary purpose is to automate the validation of research papers (PDFs) against predefined conference guidelines.

## High-Level Workflow

The validation process follows a linear, pipeline-based approach:

1. **Upload & Entry Point:**
   A user uploads a PDF via the web interface or the API endpoint (`/validate` in `app/routes.py`). The file is temporarily saved in the `temp/` directory.

2. **Validation Service (`app/services/validator_service.py`):**
   This is the orchestrator of the entire process. When `main(file_path)` is called, it triggers the following steps in sequence:
   
   - **Extraction (`extraction`):** The PDF is passed to the Extractor processor, which parses the PDF into a structured JSON representation encompassing text, fonts, layout spans, metadata, and tables. This JSON is saved temporarily and loaded back.
   - **Checkers Execution:** A series of modular checker functions are executed sequentially on the extracted JSON data. Examples include:
     - `check_express_validation`: Verifies the PDF metadata.
     - `check_title`: Validates the title format.
     - `check_abstract`, `check_keywords`, `check_h1`, `check_h2`, `check_table`, `check_references`, `check_no_of_pages`.
   - **Logging & State:** As checkers run, any detected violations are logged via the central `Logger` utility (`app/utils/logger.py`). The logger stores the error message, the specific provider (checker name), and the exact physical span `[x, y, w, h]` on the page where the error occurred.
   - **Rendering (`render_pdf_from_extracted`):** Finally, a new PDF (`rendered_output.pdf`) is generated. The system reconstructs the PDF from the extracted text spans and draws a red highlight over any text spans that were flagged by the logger as containing errors.

3. **Response:**
   - If accessed via the web interface, a user-friendly HTML page (`index.html`) is rendered, displaying the logs (often mapped to a readable report) and providing a download link for the annotated PDF.
   - If accessed via the API, a JSON response is returned with the validation status (`pass` or `fail`) and the raw logs.

## Directory Structure

```text
ictest-format-checker/
│
├── run.py                 # Application entry point
├── requirements.txt       # Python dependencies
├── app/
│   ├── __init__.py        # Flask app factory
│   ├── routes.py          # API and Web endpoints
│   ├── checkers/          # Logic for validating specific document parts (Title, Headings, etc.)
│   ├── configs/           # Error messages and guideline constants
│   ├── processors/        # PDF extraction and text parsing logic
│   ├── services/          # Core orchestration, PDF rendering, and reporting
│   ├── utils/             # Logger, span finding utilities
│   └── templates/         # HTML templates (index.html)
└── docs/                  # Documentation
```

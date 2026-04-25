# Usage Guide

The ICTEST Format Checker provides multiple ways to validate research papers depending on your workflow. You can use the interactive web interface, integrate it programmatically via the API, or batch-process entire folders of PDFs via the command line.

---

## 1. Web Interface

The web interface provides a simple, interactive way to upload a single PDF and view its validation results immediately.

**How to use:**
1. Start the Flask application:
   ```bash
   flask run
   ```
2. Open your web browser and navigate to `http://localhost:5000/`.
3. Click "Browse" or "Choose File" and select your PDF paper.
4. Click "Upload & Validate".
5. The page will reload displaying:
   - The overall Pass/Fail status.
   - A detailed breakdown of the formatting checks and any errors found.
   - A download link to retrieve the annotated PDF (`rendered_output.pdf`) with red highlights showing exactly where the errors are located on the pages.

---

## 2. API Endpoint

The REST API allows you to integrate the validation engine into other applications or scripts.

**Endpoint:** `POST /validate`

**How to use (cURL):**
```bash
curl \
  --request POST \
  --url http://localhost:5000/validate \
  --header 'content-type: multipart/form-data' \
  --form file=@your_paper.pdf
```

**Response Format:**
The API returns a JSON response containing the status and the raw array of validation logs.
```json
{
  "status": "success",
  "validation": "pass",
  "logs": [
    {
      "provider": "TITLE CHECKER",
      "error": "Title must be centered",
      "span": [72.0, 100.5, 450.0, 120.0],
      "page": 0,
      "msg_type": "INFO"
    }
  ]
}
```

---

## 3. Batch Processing (Folder Validation)

If you have multiple papers to validate (e.g., all submissions for a conference track), you can use the `folder_validate.py` script. This script processes all `.pdf` files in a given directory and generates individual reports and annotated PDFs.

**How to use:**
Run the script from your terminal, passing the path to the folder containing your PDFs:

```bash
python folder_validate.py path/to/your/pdf/folder
```

**Output Structure:**
The script will automatically create two subdirectories within your input folder: `logs/` and `output/`.

```text
path/to/your/pdf/folder/
├── paper1.pdf
├── paper2.pdf
├── logs/
│   ├── paper1.log                 # Technical stdout/stderr trace
│   └── paper2.log
└── output/
    ├── paper1_validated.pdf       # Annotated PDF with red error highlights
    ├── paper1_report.md           # User-friendly Markdown validation report
    ├── paper2_validated.pdf
    └── paper2_report.md
```

**What it does:**
For every `.pdf` file found:
1. It runs the complete validation suite.
2. It generates a human-readable markdown report (`_report.md`) detailing the issues.
3. It generates the annotated PDF (`_validated.pdf`).
4. It redirects standard console output to a `.log` file for debugging purposes.

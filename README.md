# Paper format validation for ICTEST

---
### Description

A Flask-based API and web interface for syntax-based format validation of research papers submitted to [ICTEST](https://ictest.in/). It checks PDF files against standard guidelines (like IEEE formatting) by extracting text and styles using PyMuPDF and running a series of custom validation checkers. 

**For detailed documentation regarding the architecture, extraction pipeline, validation checkers, and logging system, please refer to the [docs/README.md](docs/README.md) directory.**

### Setup

```bash
git clone https://github.com/n1ved/ictest-paper-validator.git
cd ictest-paper-validator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

### Usage

There are three main ways to use the ICTEST Format Checker: **Web Interface**, **API**, and **Batch Processing**. 

**For full details on each method, including the batch processing script (`folder_validate.py`), please see the [Usage Guide](docs/usage.md).**

**Web Interface:**
Simply navigate to `http://localhost:5000/` in your browser to upload a PDF and view the validation report and annotated output PDF directly.

**API Endpoint:**

```bash
curl \
  --request POST \
  --url http://localhost:5000/validate \
  --header 'content-type: multipart/form-data' \
  --form file=@your_paper.pdf
```

```json
{
  "logs": [
    {
      "error": "Error description",
      "provider": "VALIDATOR_NAME",
      "span": [0, 0, 0, 0],
      "page": 0,
      "msg_type": "INFO"
    }
  ],
  "status": "success",
  "validation": "pass" | "fail"
}
```

### Checks Performed

- [x] PDFeXpress Certification
- [x] Title Format
- [x] Authors (Extraction only currently)
- [x] Abstract Format
- [x] Keyword Format
- [x] Headings Order and Format (H1, H2)
- [x] Tables
	- [x] Order
	- [ ] Format
- [x] References
	- [x] Order
	- [ ] Format
- [ ] Figures
  -  [ ] is properly labeled
  -  [ ] is properly referenced
- [ ] Equations
  - [ ] format


# Paper format validation for ICTEST

---
### Description

A Flask-based API for syntax-based format validation of papers submitted to [ICTEST](https://ictest.in/).  

### Setup

```bash
git clone https://github.com/n1ved/ictest-paper-validator.git
cd ictest-paper-validator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

### API usage

```bash
curl 
  --request POST \
  --url http://localhost:5000/validate \
  --header 'content-type: multipart/form-data' \
  --form file=@file
```

```json
{
  "logs": [
    {
      "error": string,
      "provider": string,
      "span": string | null
    }
  ],
  "status": "success"
  "validation" : "pass" | "fail"
}
```

### Checks Performed

- [x] PDFeXpress Certification
- [x] Title Format
- [ ] Author
  - [ ] Validate whether its same registered authors for ICTEST
  - [ ] Format
- [x] Abstract Format
- [x] Keyword Format
- [x] Headings Order and Format
- [ ] Tables
	- [x] Order
	- [ ] Format
- [ ] Reference
	- [x] Order
	- [ ] Format
- [ ] Figures
  -  [ ] is properly labeled
  -  [ ] is properly referenced
- [ ] Equations
  - [ ] format


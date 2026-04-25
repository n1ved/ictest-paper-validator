# Formatting Checkers

The core logic of the validation system resides in the `app/checkers/` directory. Each checker is responsible for a specific component of the research paper and verifies that it adheres to the expected formatting rules.

## General Checker Workflow
Most checkers operate on the `formatted_text` array extracted from the PDF. They typically follow this pattern:
1. **Locate:** Find the specific section or element in the document (e.g., finding the text "Abstract" or scanning for Level 1 headings).
2. **Analyze Spans:** Inspect the `font`, `size`, `flags` (bold/italic), and `text` content of the relevant spans.
3. **Validate:** Compare the extracted attributes against predefined constants in `app/configs/guidelines.py` or `app/configs/errors.py`.
4. **Log Errors:** If a violation is found, use `errorlogger(provider, error_message, span)` to record the issue and mark the exact physical location of the error for later PDF rendering.

## Available Checkers

### 1. Title Checker (`title_checker.py`)
Validates the main title of the paper.
- **Rules:** Checks if the title is centered, uses a specific font size, and is properly capitalized (Title Case).

### 2. Abstract Checker (`abstract_checker.py`)
Validates the Abstract section.
- **Rules:** 
  - Ensures the word "Abstract" is present and styled correctly (usually bold/italic).
  - Validates the font size and style of the abstract body text.
  - Checks alignment and indentation rules if applicable.

### 3. Keyword Checker (`keyword_checker.py`)
Validates the Keywords section, typically following the Abstract.
- **Rules:**
  - Ensures the keyword label (e.g., "Keywords—" or "Index Terms—") is styled correctly (often bold/italic).
  - Verifies the font size of the keywords themselves.
  - Checks if keywords are in alphabetical order and properly separated.

### 4. Headings Checker (`heading_checker.py`)
Validates the structure and styling of section and subsection headings.
- **H1 Validator:** Checks Level 1 headings (e.g., "I. INTRODUCTION"). Validates Roman numeral numbering, capitalization (often All Caps or Small Caps), font size, and centering/alignment.
- **H2 Validator:** Checks Level 2 headings (e.g., "A. Background"). Validates alphabetical numbering, Title Case, font size, and italicization.
- **Order:** Ensures headings follow a logical, sequential order without skipping numbers/letters.

### 5. Table Checker (`table_checker.py`)
Validates the presence and numbering of tables.
- **Rules:** Checks if table captions (e.g., "TABLE I") follow the correct numbering sequence (Roman numerals usually). *Note: Full format validation of tables is complex and often partially implemented.*

### 6. Reference Checker (`reference_checker.py`)
Validates the References section.
- **Rules:** 
  - Locates the "References" heading.
  - Checks the numbering of references (e.g., `[1]`, `[2]`).
  - Ensures reference numbers are sequential and none are skipped or duplicated.

### 7. Author Checker (`author_checker.py`)
Currently functions primarily as an extractor.
- **Rules:** Extracts author names, affiliations, and email addresses from the beginning of the document. Future implementations may validate these against registered author lists.

### 8. Equation & Figure Checkers (`equation_checker.py`, `fig_checker.py`)
These checkers handle equations and figures.
- **Rules:** Verify that equations are numbered sequentially (e.g., `(1)`) and that figure captions (e.g., `Fig. 1.`) are numbered sequentially and styled correctly. *Note: Figure validation based solely on text extraction can be unreliable.*

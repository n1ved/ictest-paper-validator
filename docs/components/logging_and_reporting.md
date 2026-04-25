# Logging and Reporting

The ICTEST Format Checker does more than just return a boolean pass/fail status. It provides detailed feedback to the user on exactly what failed and where. This is handled by the logging, reporting, and rendering modules.

## The Logger Utility (`app/utils/logger.py`)

The `Logger` class is a central state manager that holds all logs generated during a single validation run.

### Error Logging Structure
When a checker detects a formatting violation, it calls `errorlogger(provider, error_message, span)`.
- `provider`: A string identifying the checker (e.g., "H1_VALIDATOR").
- `error_message`: A descriptive string from `app/configs/errors.py`.
- `span`: The specific text span object (containing the `bbox`, `page`, etc.) where the error was found.

The `Logger` translates this span into a physical "locator" (`page`, `block`, `line`, `span` indices) using `find_span_location` and stores it in `Logger.error_spans`.

### Console Output
The logger also handles printing colored output to the console (Terminal) depending on the configured log level:
- `printinfo` (Blue)
- `printsuccess` (Green)
- `printwarn` (Yellow)
- `printfail` (Red)

## Report Generation (`app/services/report_generator.py`)

Raw error logs are technical and often tied directly to span coordinates. The `ReportGenerator` class takes the raw logs stored by the `Logger` and translates them into a user-friendly Markdown report.

- **Provider Mapping**: Technical provider names like "H1_VALIDATOR" are mapped to friendly names like "Section Headings (Level 1)".
- **Error Cleaning**: Technical python errors are caught and replaced with helpful user instructions.
- **Aggregation**: If the same error occurs multiple times, it is grouped together (e.g., "- Title is not centered (3 occurrences)").

The resulting markdown string can be displayed on the web interface or saved as a `.md` file.

## PDF Rendering (`app/services/pdf_renderer.py`)

To provide the most direct feedback possible, the system generates an annotated PDF showing exactly where the errors are.

1. **Canvas Setup**: Uses `reportlab.pdfgen.canvas` to create a new A4 PDF (`rendered_output.pdf`).
2. **Watermarking**: Draws a large diagonal watermark ("CORRECTION REFERENCE...") to prevent users from accidentally submitting the generated error report as their final paper.
3. **Reconstruction**: Iterates through the *entire* `formatted_text` array (every page, block, line, and span) extracted initially by PyMuPDF.
4. **Drawing Text**: For every span, it checks `is_error_span` to see if that exact locator exists in `Logger.error_spans`.
   - If **NO**: It draws the text at the span's original `(x, y)` coordinates using the original mapped font and size.
   - If **YES**: It changes the fill color to red (`RGB(1,0,0)`) and draws the text, effectively highlighting the specific formatting error directly on the reconstructed document.

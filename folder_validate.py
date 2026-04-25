import os
import sys
import logging
from pathlib import Path
import shutil
from contextlib import redirect_stdout, redirect_stderr
from app.services import validator_service  # Assuming validator_service.main exists
from app.utils.logger import LogLevel, set_log_level

# Constants for folder names
LOG_FOLDER_NAME = "logs"
OUTPUT_FOLDER_NAME = "output"
DEFAULT_OUTPUT_FILE = "rendered_output.pdf"


def setup_directories(log_dir, output_dir):
    """Create necessary directories if they don't exist."""
    log_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

def move_generated_file(output_dir, paper_file_stem):
    """Move the default `rendered_output.pdf` file to the appropriate location in the output directory."""
    source_file = Path(DEFAULT_OUTPUT_FILE)
    if source_file.exists():
        target_file = output_dir / f"{paper_file_stem}_validated.pdf"
        shutil.move(str(source_file), str(target_file))
        print(f"Moved rendered output to: {target_file}")
    else:
        print(f"Warning: {DEFAULT_OUTPUT_FILE} not found after processing {paper_file_stem}. Validation may have failed.")


def validate_folder(input_folder):
    """Validate all papers in the provided folder."""
    # Set log level to INFO to suppress debug output
    set_log_level(LogLevel.INFO)

    input_folder = Path(input_folder)

    log_dir = input_folder / LOG_FOLDER_NAME
    output_dir = input_folder / OUTPUT_FOLDER_NAME
    setup_directories(log_dir, output_dir)

    for paper_file in input_folder.iterdir():
        if paper_file.is_file() and paper_file.suffix.lower() == ".pdf":  # Assuming only PDFs are valid
            log_file = log_dir / f"{paper_file.stem}.log"
            output_pdf_path = output_dir / f"{paper_file.stem}_validated.pdf"

            with open(log_file, "w") as lf, redirect_stdout(lf), redirect_stderr(lf):  # Redirect output to log file
                from app.utils.logger import Logger
                Logger.clear_logs()
                
                print(f"Processing file: {paper_file}")
                try:
                    # Call the validation service and store output
                    is_valid = validator_service.main(str(paper_file), log=True)
                    print(f"Validation {'PASSED' if is_valid else 'FAILED'} for {paper_file}")
                    
                    # Generate Report
                    from app.utils.logger import Logger
                    from app.services.report_generator import ReportGenerator
                    
                    logs = Logger.get_logs()
                    
                    # Generate Markdown Report
                    md_report_content = ReportGenerator.generate_report(paper_file.name, is_valid, logs)
                    md_report_file = output_dir / f"{paper_file.stem}_report.md"
                    with open(md_report_file, "w") as rf:
                        rf.write(md_report_content)
                        
                    # Generate HTML Report
                    html_report_content = ReportGenerator.generate_html_report(paper_file.name, is_valid, logs)
                    html_report_file = output_dir / f"{paper_file.stem}_report.html"
                    with open(html_report_file, "w") as rf:
                        rf.write(html_report_content)
                    
                    # Log report generation (will show in cleanup log mode or debug)
                    # print(f"Report generated: {report_file}") # Optional, suppressed by redirec_stdout anyway
                    
                except Exception as e:
                    print(f"Validation ERROR for {paper_file}: {e}")
                finally:
                    move_generated_file(output_dir, paper_file.stem)


def main():
    """Main entry point for the script."""
    if len(sys.argv) != 2:
        print("Usage: python folder_validate.py <folder_path>")
        sys.exit(1)

    input_folder = sys.argv[1]

    if not os.path.exists(input_folder) or not os.path.isdir(input_folder):
        print(f"Invalid folder path: {input_folder}")
        sys.exit(1)

    validate_folder(input_folder)
    print(f"Validation complete. Check 'logs/' and 'output/' in the specified folder.")


if __name__ == "__main__":
    main()
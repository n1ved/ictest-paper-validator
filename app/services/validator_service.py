from app.checkers import heading_checker, keyword_checker, abstract_checker, table_checker
from app.checkers.reference_checker import ref_validator
from app.configs.errors import PDFEXPRESS_NOT_VALIDATED
from app.processors import extractor
# import fig_checker
from app.configs.guidelines import GLOBAL_CREATOR_NAME, MIN_PAGES, MAX_PAGES
from app.services.pdf_renderer import render_pdf_from_extracted, add_watermark
from app.utils.logger import printinfo, printsuccess, printfail, errorlogger
import json

from app.checkers.title_checker import validate_title

def extraction(log , pdf_path):
    provider = "EXTRACTOR"
    if log:
        printinfo(provider, "STARTED")
    pdf_path = pdf_path
    output_file = "../../extracted_pdf_data.json"
    try:
        if log:
            printinfo(provider, "EXTRACTING FROM " + pdf_path)
        extracted_data = extractor.comprehensive_pdf_extraction(pdf_path, log=log)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=2, ensure_ascii=False, default=str)
        with open(pdf_path+'.json', 'w',encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=2, ensure_ascii=False, default=str)
        if log:
            printsuccess(provider, "EXTRACTION COMPLETED")
    except Exception as e:
        printfail(provider, str(e))

def jsonloader(log):
    if log:
        printinfo("JSONLOADER", "STARTED")
    try:
        with open('../../extracted_pdf_data.json', 'r') as file:
            data = json.load(file)
        if log:
            printsuccess("JSONLOADER", "LOADED JSON DATA")
        return data
    except Exception as e:
        printfail("JSONLOADER", str(e))
        return None

def check_express_validation(data, log):
    if log:
        printinfo("PDFEXPRESS_VALIDATION", "STARTED")
    try:
        creator_inf = data['metadata']['metadata']['creator']
        if GLOBAL_CREATOR_NAME.lower() not in creator_inf.lower():
            printfail("PDFEXPRESS_VALIDATION", f"Creator name '{creator_inf}' does not match expected '{GLOBAL_CREATOR_NAME}'")
            errorlogger('PDFEXPRESS_VALIDATION', PDFEXPRESS_NOT_VALIDATED)
            return False
        if log:
            printsuccess("PDFEXPRESS_VALIDATION", "PDFExpress validation passed")
        return True
    except Exception as e:
        printfail("PDFEXPRESS_VALIDATION", str(e))
        return False



def check_title(data,log):
    try:
        return validate_title(data,log)
    except Exception as e:
        printfail("TITLE CHECKER", str(e))
        return False


def check_abstract(data,log):
    try:
        spans = abstract_checker.extract_abstract_spans(data['formatted_text'][0])
        return abstract_checker.validate_abstract_format(spans)
    except Exception as e:
        printfail("ABSTRACT CHECKER", str(e))
        return False

def check_keywords(data, log):
    try:
        keywords_spans = keyword_checker.extract_keywords(data['formatted_text'][0])
        return keyword_checker.validate_keywords_format(keywords_spans)
    except Exception as e:
        printfail("KEYWORDS CHECKER", str(e))
        return False

def check_h1(data, log):
    provider = 'H1_VALIDATOR'
    if log:
        printinfo(provider, "STARTED")
    try:
        formatted_text = data['formatted_text']
        return heading_checker.h1_validator(formatted_text, log=log)
    except Exception as e:
        printfail(provider, f"Error during H1 validation: {str(e)}")
        return False

def check_h2(data, log):
    provider = 'H2_VALIDATOR'
    if log:
        printinfo(provider, "STARTED")
    try:
        formatted_text = data['formatted_text']
        return heading_checker.h2_validator(formatted_text, log=log)
    except Exception as e:
        printfail(provider, f"Error during H2 validation: {str(e)}")
        return False

# WONTFIX : UNRELIABLE
# def check_figures(data, log):
#     provider = 'FIGURE_VALIDATOR'
#     if log:
#         printinfo(provider, "STARTED")
#     try:
#         formatted_text = data['formatted_text']
#         count = data['images']
#         return fig_checker.figure_validator(formatted_text,count,log=log)
#     except Exception as e:
#         printfail(provider, f"Error during figure validation: {str(e)}")
#         return False

def check_table(data, log):
    provider = 'TABLE_VALIDATOR'
    printinfo(provider, "STARTED")
    try:
        formatted_text = data['formatted_text']
        return table_checker.table_validator(formatted_text, len(data['tables']))
    except Exception as e:
        printfail(provider, f"Error during table validation: {str(e)}")
        return False

def check_references(data, log):
    provider = 'REF_VALIDATOR'
    if log:
        printinfo(provider, "STARTED")
    try:
        text_content = data['text_content']
        return ref_validator(text_content)
    except Exception as e:
        printfail(provider, f"Error during reference validation: {str(e)}")
        return False

def check_no_of_pages(data, log):
    provider = 'PAGE_VALIDATOR'
    if log:
        printinfo(provider, "STARTED")
    try:
        page_count = len(data['text_content'])
        if page_count < MIN_PAGES or page_count > MAX_PAGES:
            printfail(provider, f"Invalid number of pages: {page_count}")
            errorlogger(provider, f"Invalid number of pages: {page_count}")
            return False
        if log:
            printsuccess(provider, f"Page count validation passed: {page_count} pages")
        return True
    except Exception as e:
        printfail(provider, f"Error during page count validation: {str(e)}")
        return False

def main(paper,log = False):
    print()
    total_valid = True
    extraction(log , paper)
    data = jsonloader(log)
    total_valid &= check_express_validation(data,log)
    total_valid &= check_no_of_pages(data,log)
    total_valid &= check_title(data,log)
    total_valid &= check_abstract(data,log)
    total_valid &= check_keywords(data,log)
    total_valid &= check_h1(data,log)
    total_valid &= check_h2(data,log)
    # total_valid &= check_figures(data,log)
    total_valid &= check_table(data,log)
    total_valid &= check_references(data,log)
    render_pdf_from_extracted(data,'rendered_output.pdf')
    if log:
        printsuccess("MAIN" , f"Total validation result: {'Pass' if total_valid else 'Fail'}")
    return total_valid


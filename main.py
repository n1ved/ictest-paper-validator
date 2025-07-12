from checkers import abstract_checker, heading_checker, keyword_checker, table_checker
from processors import extractor
# import fig_checker
from configs.guidelines import GLOBAL_CREATOR_NAME
from utils.logger import printinfo, printsuccess, printfail
import json

from checkers.title_checker import validate_title

def extraction(log , pdf_path):
    provider = "EXTRACTOR"
    if log:
        printinfo(provider, "STARTED")
    pdf_path = pdf_path
    output_file = "./extracted_pdf_data.json"
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
        with open('extracted_pdf_data.json', 'r') as file:
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


def main(paper,log = False):
    print()
    total_valid = True
    extraction(log , paper)
    data = jsonloader(log)
    total_valid &= check_express_validation(data,log)
    total_valid &= check_title(data,log)
    total_valid &= check_abstract(data,log)
    total_valid &= check_keywords(data,log)
    total_valid &= check_h1(data,log)
    total_valid &= check_h2(data,log)
    # total_valid &= check_figures(data,log)
    total_valid &= check_table(data,log)
    if log:
        printsuccess("MAIN" , f"Total validation result: {'Pass' if total_valid else 'Fail'}")
    return total_valid


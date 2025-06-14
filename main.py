import extractor
from guidelines import TITLE_FLAGS, TITLE_FONT_SIZES
from logger import printinfo, printsuccess, printfail
import title_checker
import json
import re

from title_checker import validate_title


def extraction(log , pdf_path):
    provider = "EXTRACTOR"
    if log:
        printinfo(provider, "STARTED")
    pdf_path = pdf_path
    output_file = "./extracted_pdf_data.json"
    try:
        if log:
            printinfo(provider, "EXTRACTING FROM " + pdf_path)
        extracted_data = extractor.comprehensive_pdf_extraction(pdf_path,log=log)
        with open(output_file, 'w', encoding='utf-8') as f:
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


def check_title(data,log):
    try:
        return validate_title(data,log)
    except Exception as e:
        printfail("TITLE CHECKER", str(e))
        return False


# def check_abstract(log):
#     if log:
#         print("**Starting abstract checker...")
#     with open('extracted_pdf_data.json','r') as file:
#         data = json.load(file)
#         first_page_contents = data['text_content'][0]['text']
#         pattern = r'abstract(.*?)keyword'
#         matches = re.findall(pattern, first_page_contents , re.IGNORECASE | re.DOTALL)
#         largest = matches[0]
#         for i,match in enumerate(matches , 1):
#             if len(largest) < len(match):
#                 largest = match
#         split_abstract = largest.split()
#         for i in range(0,len(split_abstract)):



def main(log = False):
    for i in range(0,3):
        print('\n\033[95m\033[1m' + '[[[[[ ICTEST-CHECKER EXPERIMENTAL RUN ' + str(i) + ' ]]]]]\033[0m\n\n')
        total_valid = True
        extraction(log , "papers/" + str(i) + ".pdf")
        data = jsonloader(log)
        total_valid &= check_title(data,log)
        # check_abstract(log)
        if log:
            print(f"Total validation result: {'Pass' if total_valid else 'Fail'}")
    return None

main(log = True)

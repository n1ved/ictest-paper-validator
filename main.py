import extractor
import title_checker
import json
import re


def extraction(log):
    if log:
        print("Starting main function...")
    pdf_path = "papers/1.pdf"
    output_file = "./extracted_pdf_data.json"
    try:
        if log:
            print("**Extracting data from PDF...")
        extracted_data = extractor.comprehensive_pdf_extraction(pdf_path,log=log)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=2, ensure_ascii=False, default=str)
        if log:
            print("**Finished extracting data from PDF.")
    except Exception as e:
        print(f"An error occurred: {e}")


def check_title(log):
    if log:
        print("**Starting title checker...")
    with open('extracted_pdf_data.json', 'r') as file:
        data = json.load(file)
        title = data['metadata']['metadata']['title']
        if log:
            print(f"Title: {title}")

    result = title_checker.validate_title(title)

    if log:
        print(f"Title validation result: {"Pass" if result else "Fail"}")
        print("**Finished title checker.")
    return result

def check_abstract(log):
    if log:
        print("**Starting abstract checker...")
    with open('extracted_pdf_data.json','r') as file:
        data = json.load(file)
        first_page_contents = data['text_content'][0]['text']
        pattern = r'abstract(.*?)keyword'
        matches = re.findall(pattern, first_page_contents , re.IGNORECASE | re.DOTALL)
        if log:
            for i,match in enumerate(matches , 1):
                print(f"Match {i} : {match}\n")

def main(log = False):
    total_valid = True
    extraction(log)
    total_valid &= check_title(log)
    check_abstract(log)
    if log:
        print(f"Total validation result: {'Pass' if total_valid else 'Fail'}")
    return total_valid


main(log = True)

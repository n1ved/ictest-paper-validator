from guidelines import PAGE_SMALLEST_MARGIN, H1_INDEX_FONT_SIZES, H1_INDEX_FLAGS, H1_FIRST_FONT_SIZES, \
    H1_REST_FONT_SIZES, H1_REST_FLAGS, H1_FIRST_FLAGS
from logger import printinfo, printfail, printsuccess, printwarn

provider = 'H1_VALIDATOR'

def extract_h1(formatted_text):
    printinfo('H1_VALIDATOR', "STARTED extraction")
    roman_numerals = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x' , 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx']
    h1_spans = []
    in_h1 = 0
    found_h1 = False
    for page in formatted_text:
        for block in page['blocks']:
            for line in block['lines']:
                if line['bbox'][0] >= PAGE_SMALLEST_MARGIN :
                    for span in line['spans']:
                        text = span['text'].strip().lower()

                        if len(text) <= len(roman_numerals[in_h1]) or in_h1 >= len(roman_numerals):
                            continue
                        if not(text[:len(roman_numerals[in_h1])] == roman_numerals[in_h1] and text[len(roman_numerals[in_h1])] == '.'):
                            continue
                        else:
                            found_h1 = True
                            in_h1 += 1
                            break


                    if found_h1:
                        h1_spans.append(line['spans'])
                        found_h1 = False
                        break
    printinfo('H1_VALIDATOR', "EXTRACTED H1 SPAN [ end of text ]")
    return h1_spans






def h1_validator(formatted_text, log):
    provider = 'H1_VALIDATOR'
    if log:
        printinfo(provider, "STARTED")
    try:
        h1_spans = extract_h1(formatted_text)
        if not h1_spans:
            printinfo(provider, "No H1 spans found")
            return False
        valid = True
        for span in h1_spans:
            count = 0
            cur_h1 = ""
            local_valid = False
            for s in span:
                if count == 0:
                    if round(s['size']) in H1_INDEX_FONT_SIZES and s['flags'] in H1_INDEX_FLAGS and "".join(s['text'].split()).strip() != '':
                        cur_h1 += s['text'] + " "
                        count += 1
                elif count == 1:
                    if round(s['size']) in H1_FIRST_FONT_SIZES and s['flags'] in H1_FIRST_FLAGS and "".join(s['text'].split()).strip() != '':
                        cur_h1 += s['text'] + " "
                        count += 1
                elif count == 2:
                    if round(s['size']) in H1_REST_FONT_SIZES and s['flags'] in H1_REST_FLAGS and "".join(s['text'].split()).strip() != '':
                        cur_h1 += s['text'] + " "
                        count += 1
                        local_valid = True
                        break
            if not local_valid:
                printfail(provider, f"H1 validation failed for span: {cur_h1.strip()} with size {s['size']} and flags {s['flags']}")
                valid = False
            else:
                printsuccess(provider, f"H1 span validated successfully: {cur_h1.strip()} with size {s['size']} and flags {s['flags']}")
        if valid:
            printsuccess(provider, "All H1 spans validated successfully")
            return True
        return False
    except Exception as e:
        printfail(provider, f"Error during H1 validation: {str(e)}")
        return False





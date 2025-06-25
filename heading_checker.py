from guidelines import PAGE_SMALLEST_MARGIN, H1_INDEX_FONT_SIZES, H1_INDEX_FLAGS, H1_FIRST_FONT_SIZES, \
    H1_REST_FONT_SIZES, H1_REST_FLAGS, H1_FIRST_FLAGS, check_font, H2_FONT_SIZES, PAGE_SECOND_BLOCK_MARGIN
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


def extract_h2(formatted_text):
    printinfo(provider , "STARTED H2 extraction")
    h2_letter_indeces = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    h2_spans = []
    in_h2 = 0
    found_h2 = False
    for page in formatted_text:
        for block in page['blocks']:
            for line in block['lines']:
                if line['bbox'][0] <= PAGE_SMALLEST_MARGIN or line['bbox'][0] >= PAGE_SECOND_BLOCK_MARGIN:
                    for span in line['spans']:
                        text = span['text'].strip()
                        if len(text) < 2:
                            continue
                        if text[0] == h2_letter_indeces[in_h2] and text[1] == '.':
                            printinfo(provider, f"Found H2 span: {text[:2]}")
                            found_h2 = True
                            in_h2 += 1
                            break
                        elif text[0] == 'A' and text[1] == '.':
                            printinfo(provider, f"Found H2 span: {text[:2]} (A.)")
                            found_h2 = True
                            in_h2 = 1
                            break
                    if found_h2:
                        h2_spans.append(line['spans'])
                        found_h2 = False
                        break
    printinfo(provider, "EXTRACTED H2 SPAN [ end of text ]")
    return h2_spans









def h1_validator(formatted_text, log):
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
                if check_font(s['font']) is False and "".join(s['text'].split()).strip() != '':
                    printfail(provider, f"Font validation failed for span: {s['text']} with font {s['font']}")
                    valid = False
                    break
                if count == 0:
                    if round(s['size']) in H1_INDEX_FONT_SIZES and s['flags'] in H1_INDEX_FLAGS and "".join(s['text'].split()).strip() != '':
                        cur_h1 += s['text'] + " "
                        if len(cur_h1) > len(cur_h1[:(cur_h1.find('.')+1)]):
                            count += 2
                        else:
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

def h2_validator(formatted_text, log):
    if log:
        printinfo(provider, "STARTED")
    try:
        h2_spans = extract_h2(formatted_text)
        if not h2_spans:
            printinfo(provider, "No H2 spans found")
            return False
        valid = True
        for span in h2_spans:
            for s in span:
                if (
                    check_font(s['font']) is False and
                    "".join(s['text'].split()).strip() != '' and
                    round(s['size']) in H2_FONT_SIZES and
                    s['flags'] in H1_REST_FLAGS
                ):
                    printfail(provider, f"Font validation failed for span: {s['text']} with font {s['font']}")
                    valid = False
                    break
        if valid:
            printsuccess(provider, "All H2 spans validated successfully")
            return True
        return False
    except Exception as e:
        printfail(provider, f"Error during H2 validation: {str(e)}")
        return False




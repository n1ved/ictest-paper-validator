from guidelines import TITLE_FONT_FAMILIES, check_font
from guidelines import TITLE_FONT_SIZES
from guidelines import TITLE_FLAGS
from logger import printinfo, printfail, printwarn, printsuccess


provider = "TITLE_VALIDATOR"

def normalize(text):
    return ''.join(text.split()).lower()

def validate_title(data, log):
    if log:
        printinfo(provider,"STARTED")
    try:
        title = data['metadata']['metadata']['title']
        printinfo(provider, "Title found: " + title)

        formatted_text = data['formatted_text'][0]
        title_alt = formatted_text['blocks'][0]['lines'][0]['spans'][0]
        cursor = 1
        while '©' in title_alt['text'] or "".join(title_alt['text'].split()).strip() == '':
            printwarn(provider,"copyright symbol or blank space found in title, skipping to next block.")
            title_alt = formatted_text['blocks'][cursor]['lines'][0]['spans'][0]
            cursor += 1
        printinfo(provider, "Alt title found: " + str(title_alt['text']))

        family = title_alt['font']
        result = check_font(family=family) and \
            round(title_alt['size']) in TITLE_FONT_SIZES and \
            title_alt['flags'] in TITLE_FLAGS

        if not result:
            printwarn(provider , title_alt['font']+ "@" + str(title_alt['size']) + " with flags " + str(title_alt['flags']) + " failed validation.")
            printwarn(provider , "Alt title failed validation, checking original title...")
            title_spans = []
            local_result = True
            title_normalized = normalize(title)
            collected_title = ''
            string_found = False
            for block in formatted_text['blocks']:
                for line in block['lines']:
                    for span in line['spans']:
                        span_text = span['text']
                        collected_title += span_text
                        if title_normalized in normalize(collected_title):
                            printinfo(provider, "Title found: " + span_text + "[" + str(span['font']) + "@" + str(span['size']) + " with flags " + str(span['flags']) + "]")
                            string_found = True
                            local_result = check_font(family=span['font']) and \
                                round(span['size']) in TITLE_FONT_SIZES and \
                                span['flags'] in TITLE_FLAGS
                        if string_found:
                            break
                    if string_found:
                        break
                if string_found:
                    break


            if local_result:
                printinfo(provider, "Original title" + str(title_spans) + " passed validation.")
                result = len(title_spans) > 0 and local_result
            else:
                printfail(provider, "Original title failed validation. Title: " + str(collected_title))
                result = False
        else:
            printinfo(provider, "Alt title passed validation: " + str(title_alt['text']))
        if result:
            printsuccess(provider, "TITLE CHECKER passed validation.")
        return result

    except Exception as e:
        printfail("TITLE CHECKER", str(e))
        return False


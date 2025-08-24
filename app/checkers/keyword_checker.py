from app.configs.errors import KEYWORD_NOT_FOUND, KEYWORD_VALIDATION_FAILED
from app.configs.guidelines import check_font, KEYWORDS_FONT_SIZES, KEYWORDS_FLAGS, GLOBAL_IGNORE_CHARS
from app.utils.logger import printinfo, printfail, errorlogger

provider = 'KEYWORD_VALIDATOR'

def extract_keywords(formatted_text):
    printinfo(provider, "STARTED extraction")
    keywords_spans = []
    in_keywords = False
    for block in formatted_text['blocks']:
        for line in block['lines']:
            for span in line['spans']:
                text = span['text'].strip().lower()
                if not in_keywords:
                    if 'keywords' in text or 'index terms' in text:
                        keywords_spans.append(span)
                        in_keywords = True
                        continue
                else:
                    if 'i.' in text:
                        printinfo(provider, "EXTRACTED KEYWORD SPAN [ 'I.' found ]")
                        return keywords_spans
                    elif ''.join(text.split()).strip() in GLOBAL_IGNORE_CHARS:
                        continue
                    keywords_spans.append(span)
    printinfo(provider, "EXTRACTED KEYWORD SPAN [ end of text ]")
    return keywords_spans

def validate_keywords_format(keywords_spans):
    printinfo(provider, "STARTED validation")
    if not keywords_spans:
        printfail(provider, "No keywords spans found")
        errorlogger(
            provider,
            KEYWORD_NOT_FOUND
        )
        return False
    for span in keywords_spans:
        if not (
            check_font(span['font']) and
            round(span['size']) in KEYWORDS_FONT_SIZES and
            span['flags'] in KEYWORDS_FLAGS
        ):
            printfail(provider, "Failed at span: " + " [" + span['text'] + "][" + span['font'] + "@" + str(span['size']) + " with flags " + str(span['flags']) + "]")
            errorlogger(
                provider,
                KEYWORD_VALIDATION_FAILED,
                span['text']
            )
            return False
    printinfo(provider, "All spans validated")
    return True
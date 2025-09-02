from app.configs.errors import ABSTRACT_VALIDATION_FAILED, ABSTRACT_NOT_FOUND
from app.configs.guidelines import check_font, ABSTRACT_FONT_SIZES, ABSTRACT_FLAGS, GLOBAL_IGNORE_CHARS
from app.utils.logger import printfail, printsuccess, printinfo, errorlogger

provider = 'ABSTRACT_VALIDATOR'

def extract_abstract_spans(formatted_text):
    printinfo(provider,"STARTED extraction")
    abstract_spans = []
    in_abstract = False
    for block in formatted_text['blocks']:
        for line in block['lines']:
            for span in line['spans']:
                text = span['text'].strip().lower()
                if not in_abstract:
                    if 'abstract' in text:
                        in_abstract = True
                        continue
                else:
                    if 'keyword' in text or 'keywords' in text or 'index terms' in text:
                        printsuccess(provider,"EXTRACTED ABSTRACT SPAN [ keyword found ]")
                        return abstract_spans
                    elif ''.join(text.split()).strip() == '':
                            continue
                    abstract_spans.append(span)
    printsuccess(provider,"EXTRACTED ABSTRACT SPAN [ end of text ]")
    if not abstract_spans:
        printfail(provider,"No abstract spans found")
        errorlogger(
            provider,
            ABSTRACT_NOT_FOUND
        )
        return []
    return abstract_spans

def validate_abstract_format(abstract_spans):
    printinfo(provider, "STARTED validation")
    for span in abstract_spans:
        if span['text'].strip() in GLOBAL_IGNORE_CHARS:
            continue
        elif not (
            check_font(span['font']) and
            round(span['size']) in ABSTRACT_FONT_SIZES
            and span['flags'] in ABSTRACT_FLAGS
        ):
            printfail(provider,"Failed at span: " + " ["+span['text']+"][" + span['font'] + "@" + str(span['size']) + " with flags " + str(span['flags']) + "]")
            errorlogger(
                provider,
                ABSTRACT_VALIDATION_FAILED,
                span,
            )
            return False
    printsuccess(provider,"All spans validated")
    return True

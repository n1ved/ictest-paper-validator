from app.configs.guidelines import FIG_CAPTION_SIZES, FIG_CAPTION_FLAGS
from app.utils.logger import printfail, printsuccess, printwarn, printinfo

provider = 'FIGURE_VALIDATOR'

def figure_validator(formatted_text,count, log):
    try:
        fig_count = 0
        for page in formatted_text:
            for block in page['blocks']:
                for line in block['lines']:
                    for span in line['spans']:
                        text = span['text'].strip()
                        if len(text) < 5:
                            continue
                        if text[:4] == 'Fig.' and \
                                text[5].isdigit() and \
                                round(span['size']) in FIG_CAPTION_SIZES and \
                                span['flags'] in FIG_CAPTION_FLAGS:
                            if text[5] == str(fig_count+1):
                                printinfo(provider, f"{text}")
                                fig_count += 1
                                continue
                            else:
                                printfail(provider, "Unexpected figure number: " + text[5] + " (expected " + str(fig_count + 1) + ")")
                                return False
                        elif (text[:4] == 'Fig.' and
                              round(span['size']) in FIG_CAPTION_SIZES):
                            printwarn(provider, "Unexpected figure number: " + text)
        if fig_count == count:
            printsuccess(provider, "All figures have been checked")
            return True
        else:
            printfail(provider, f"Figure count mismatch: expected {count}, found {fig_count}")
            return False
    except Exception as e:
        printfail(provider, f"Error during figure validation: {str(e)}")
        return 0
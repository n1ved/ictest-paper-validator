import re

from app.configs.errors import REFERENCE_ORDER_MISMATCH, REFERENCE_INVALID_LATEX
from app.utils.logger import errorlogger, printinfo


def ref_validator(text_content):
    count = 1
    provider = 'REF_VALIDATOR'
    for page in text_content:
        text = page['text'].strip()
        for word in text.split():
            if '[' in word and ']' in word:
                    if word.count('[') > 1 or word.count(']') > 1:
                        words = word.split(']')
                        words = [w.strip() for w in words]
                        words = [w for w in words if (w != '-' and w != ',')]
                        words = [w + ']' for w in words if w]
                    else:
                        words = [word]
                    try:
                        for w in words:
                            open_bracket_index = w.index('[')
                            close_bracket_index = w.index(']')
                            w = w[open_bracket_index:close_bracket_index + 1]
                            w = "".join(w.split())
                            w = w.replace('.', '').replace(';', '').strip()
                            regex_comparison_str = re.compile(r"\[\d+(?:[-,]\d+)?\]")
                            if not regex_comparison_str.fullmatch(w):
                                continue
                            pattern = re.compile(r"\[\d+\]")
                            isnum = pattern.fullmatch(w)

                            printinfo(provider, f"Processing {w} checking against {count}")
                            if isnum:
                                ref_number = int(w[1:-1])
                                if ref_number > count:
                                    errorlogger(
                                        provider,
                                        REFERENCE_ORDER_MISMATCH,
                                        f"Reference number {ref_number} is greater than expected {count}",
                                    )
                                    return False
                                else:
                                    if ref_number < count:
                                        continue
                                    count = ref_number + 1
                            elif w.find('-') != -1 or w.find(',') != -1:
                                split_char = ""
                                if w.find('-') != -1:
                                    split_char = "-"
                                elif w.find(',') != -1:
                                    split_char = ","
                                else:
                                    continue
                                ref_str = w[1:-1]
                                ref_number = int(ref_str.split(split_char)[0])
                                if ref_number > count:
                                    errorlogger(
                                        provider,
                                        REFERENCE_ORDER_MISMATCH,
                                        f"Reference number {ref_number} is greater than expected {count}",
                                    )

                                    return False
                                else:
                                    ref_num = int(ref_str.split(split_char)[1]) + 1
                                    if ref_num < count:
                                        continue
                                    count = ref_num

                            elif w.find('?'):
                                errorlogger(
                                    provider,
                                    REFERENCE_INVALID_LATEX,
                                    f"Reference number {w} is not a valid reference",
                                )
                                return False
                    except Exception as e:
                        errorlogger(
                            provider,
                            REFERENCE_INVALID_LATEX,
                            f"Error parsing reference number {w}: {str(e)}",
                        )
                        return False
    return True

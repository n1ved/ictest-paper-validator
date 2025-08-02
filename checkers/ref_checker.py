from configs.errors import REFERENCE_ORDER_MISMATCH, REFERENCE_INVALID_LATEX
from utils.logger import errorlogger


def ref_validator(text_content):
    count = 1
    provider = 'REF_VALIDATOR'
    for page in text_content:
        text = page['text'].strip()
        for word in text.split():
            if word.startswith('[') and word.endswith(']'):
                try:
                    ref_number = int(word[1:-1])
                    if ref_number.is_integer():
                        if ref_number > count:
                            errorlogger(
                                provider,
                                REFERENCE_ORDER_MISMATCH,
                                f"Reference number {ref_number} is greater than expected {count}",
                            )
                            return False
                        else:
                            count = ref_number + 1
                    elif word.find('-') != -1:
                        ref_str = word[1:-1]
                        ref_number = int(ref_str.split('-')[0])
                        if ref_number > count:
                            errorlogger(
                                provider,
                                REFERENCE_ORDER_MISMATCH,
                                f"Reference number {ref_number} is greater than expected {count}",
                            )

                            return False
                        else:
                            count = int(ref_str.split('-')[1]) + 1

                    elif word.find('?'):
                        errorlogger(
                            provider,
                            REFERENCE_INVALID_LATEX,
                            f"Reference number {word} is not a valid reference",
                        )
                        return False

                except Exception as e:
                    errorlogger(
                        provider,
                        REFERENCE_INVALID_LATEX,
                        f"Error parsing reference number {word}: {str(e)}",
                    )
                    return False
    return True

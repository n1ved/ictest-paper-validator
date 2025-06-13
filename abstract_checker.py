def extract_abstract_spans(formatted_text):
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
                    if 'keyword' in text or 'keywords' in text:
                        return abstract_spans
                    abstract_spans.append(span)
    return abstract_spans

def validate_abstract_format(abstract_spans):
    for span in abstract_spans:
        if not (
            span['font'] == 'TimesNewRoman,Bold'
            round(span['size']) == 9
            span['is_italic']
        )

# Kinda roundabout way to find span location but I don't wanna refractor the whole code rn
# Keep this here until next OOP refactor
# This also likely breaks when there are duplicate spans, but that should be rare enough
# TODO : Refactor to OOP

def find_span_location(formatted_text, target_span):
    return_data = []
    for each_span in target_span:
        for page_idx, page in enumerate(formatted_text):
            for block_idx, block in enumerate(page['blocks']):
                for line_idx, line in enumerate(block['lines']):
                    for span_idx, span in enumerate(line['spans']):
                        if all(span.get(k) == each_span.get(k) for k in ['text', 'font', 'size', 'flags', 'bbox']):
                            return_data.append({'page': page_idx, 'block': block_idx, 'line': line_idx, 'span': span_idx})
    return return_data
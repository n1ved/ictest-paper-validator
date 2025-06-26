from guidelines import TABLE_CAPTION_SIZES, TABLE_CAPTION_FLAGS
from logger import printinfo, printfail, printsuccess, printwarn
from title_checker import provider


def table_validator(formatted_text, table_count):
    provider = 'TABLE_VALIDATOR'
    printinfo(provider, "STARTED table extraction")
    table_spans = []
    roman_numerals = [
        'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
        'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX'
    ]
    in_table = 0
    prevalidate = False
    for page in formatted_text:
        for block in page['blocks']:
            for line in block['lines']:
                for span in line['spans']:
                    if round(span['size']) not in TABLE_CAPTION_SIZES or \
                        span['flags'] not in TABLE_CAPTION_FLAGS:
                        continue
                    text = "".join(span['text'].split()).strip()
                    if len(text) < 5 :
                        continue
                    if len(text) < 6 :
                        prevalidate =  roman_numerals[in_table] == line['spans'][-1]['text'].strip()
                    if text[:5] == 'TABLE':
                        printwarn(provider, f"Found table span: {span['text']}")
                        if prevalidate:
                            printinfo(provider, f"Found table span: {span['text']}")
                            prevalidate = False
                            in_table += 1
                            break
                        if len(text) < 6:
                            break
                        if text[5:(5+len(roman_numerals[in_table]))] == roman_numerals[in_table]:
                            in_table += 1
                            printinfo(provider, f"Table {roman_numerals[in_table-1]} found")
                        elif text[5] in roman_numerals:
                            printfail(provider , f"Unexpected table span: {text[:6]}. Expected: TABLE {roman_numerals[in_table]}")
    if in_table == table_count:
        printsuccess(provider, f"All {table_count} tables have been checked")
        return True
    else:
        printfail(provider, f"Table count mismatch: expected {table_count}, found {in_table}")
        return False

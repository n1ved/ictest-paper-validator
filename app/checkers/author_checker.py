
import re
from app.utils.logger import printinfo, printfail, printsuccess, infologger

provider = 'AUTHOR_EXTRACTOR'
EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+'

def extract_authors(formatted_text):
    printinfo(provider, "STARTED extraction")
    
    extracted_authors = []
    found_abstract = False
    
    for page in formatted_text:
        if found_abstract:
            break
            
        for block in page['blocks']:
            if found_abstract:
                break
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    
                    # Stop if Abstract is reached
                    if 'abstract' in text.lower():
                        found_abstract = True
                        break
                    
                    # Check for emails
                    emails = re.findall(EMAIL_REGEX, text)
                    if emails:
                        for email in emails:
                            infologger(provider, f"Found author email: {email}", msg_type='REPORT_DATA', data={'key': 'author_email', 'value': email})
                            
                            # Heuristic: The text containing the email usually has the author info or affiliation
                            # We'll just capture the whole text block for now as context
                            context = text
                            
                            extracted_authors.append({
                                'email': email,
                                'context': context
                            })

    if extracted_authors:
        printsuccess(provider, f"Extracted {len(extracted_authors)} potential author(s)")
    else:
        printinfo(provider, "No authors/emails found before Abstract")
        
    return extracted_authors

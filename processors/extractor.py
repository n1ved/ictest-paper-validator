import fitz  # PyMuPDF
import json
from pathlib import Path

from utils.logger import printinfo, printfail

provider = "PDF_EXTRACTOR"
def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file."""
    doc = fitz.open(pdf_path)
    text_content = []

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()
        text_content.append({
            'page': page_num + 1,
            'text': text
        })

    doc.close()
    return text_content

def extract_metadata(pdf_path):
    """Extract metadata from a PDF file."""
    doc = fitz.open(pdf_path)
    metadata = doc.metadata

    # Additional information
    info = {
        'metadata': metadata,
        'page_count': doc.page_count,
        'is_pdf': doc.is_pdf,
        'is_encrypted': doc.is_encrypted,
        'needs_pass': doc.needs_pass
    }

    doc.close()
    return info

def extract_tables_from_pdf(pdf_path):
    """Extract tables from a PDF file (requires pymupdf-fonts package)."""
    doc = fitz.open(pdf_path)
    tables_data = []

    for page_num in range(doc.page_count):
        try:
            page = doc[page_num]

            # Check if find_tables method exists (newer versions of PyMuPDF)
            if hasattr(page, 'find_tables'):
                # Find tables on the page
                tables = page.find_tables()

                for table_index, table in enumerate(tables):
                    try:
                        # Extract table data
                        table_data = table.extract()

                        tables_data.append({
                            'page': page_num + 1,
                            'table_index': table_index + 1,
                            'data': table_data,
                            'bbox': table.bbox if hasattr(table, 'bbox') else None
                        })
                    except Exception as e:
                        print(f"Error extracting table {table_index + 1} from page {page_num + 1}: {e}")
                        continue
            else:
                print("Table extraction not supported in this PyMuPDF version")
                break

        except Exception as e:
            print(f"Error processing page {page_num + 1} for tables: {e}")
            continue

    doc.close()
    return tables_data

def extract_links_and_annotations(pdf_path):
    """Extract links and annotations from a PDF file."""
    doc = fitz.open(pdf_path)
    links_and_annotations = []

    for page_num in range(doc.page_count):
        try:
            page = doc[page_num]

            # Extract links
            try:
                links = page.get_links()
                for link in links:
                    links_and_annotations.append({
                        'page': page_num + 1,
                        'type': 'link',
                        'bbox': link.get('from', []),
                        'uri': link.get('uri', ''),
                        'page_dest': link.get('page', '')
                    })
            except Exception as e:
                print(f"Error extracting links from page {page_num + 1}: {e}")

            # Extract annotations
            try:
                annotations = page.annots()
                for annot in annotations:
                    try:
                        annot_dict = annot.info
                        annot_dict['page'] = page_num + 1
                        annot_dict['type'] = 'annotation'
                        links_and_annotations.append(annot_dict)
                    except Exception as e:
                        print(f"Error processing annotation on page {page_num + 1}: {e}")
                        continue
            except Exception as e:
                print(f"Error extracting annotations from page {page_num + 1}: {e}")

        except Exception as e:
            print(f"Error processing page {page_num + 1} for links/annotations: {e}")
            continue

    doc.close()
    return links_and_annotations

def extract_fonts_info(pdf_path):
    """Extract font information from a PDF file."""
    doc = fitz.open(pdf_path)
    fonts_info = []

    for page_num in range(doc.page_count):
        page = doc[page_num]
        fonts = page.get_fonts()

        for font in fonts:
            fonts_info.append({
                'page': page_num + 1,
                'xref': font[0],
                'ext': font[1],
                'type': font[2],
                'basefont': font[3],
                'name': font[4],
                'encoding': font[5],
                'referenced': font[6]
            })

    doc.close()
    return fonts_info

def extract_text_with_formatting(pdf_path):
    """Extract text with formatting information."""
    doc = fitz.open(pdf_path)
    formatted_text = []

    for page_num in range(doc.page_count):
        page = doc[page_num]

        # Get text with detailed formatting
        text_dict = page.get_text("dict")

        page_content = {
            'page': page_num + 1,
            'blocks': []
        }

        for block in text_dict["blocks"]:
            if "lines" in block:  # Text block
                block_content = {
                    'bbox': block['bbox'],
                    'lines': []
                }

                for line in block["lines"]:
                    line_content = {
                        'bbox': line['bbox'],
                        'spans': []
                    }

                    for span in line["spans"]:
                        span_content = {
                            'text': span['text'],
                            'font': span['font'],
                            'size': span['size'],
                            'flags': span['flags'],  # Bold, italic, etc.
                            'color': span['color'],
                            'bbox': span['bbox']
                        }
                        line_content['spans'].append(span_content)

                    block_content['lines'].append(line_content)

                page_content['blocks'].append(block_content)

        formatted_text.append(page_content)

    doc.close()
    return formatted_text

def comprehensive_pdf_extraction(pdf_path,log=False):
    """Perform comprehensive extraction of all PDF data."""
    if log:
        printinfo(provider , f"Processing PDF: {pdf_path}")

    # Basic information
    try:
        metadata = extract_metadata(pdf_path)
        if log:
            printinfo(provider,f"PDF has {metadata['page_count']} pages")
    except Exception as e:
        printfail(provider,f"Error extracting metadata: {e}")
        return None

    # Extract different types of data
    extracted_data = {
        'metadata': metadata,
    }

    # Extract text content
    try:
        if log:
            printinfo(provider,"Extracting text content...")
        extracted_data['text_content'] = extract_text_from_pdf(pdf_path)
    except Exception as e:
        printfail(provider,f"Error extracting text: {e}")
        extracted_data['text_content'] = []

    # Extract formatted text
    try:
        if log:
            printinfo(provider,"Extracting formatted text...")
        extracted_data['formatted_text'] = extract_text_with_formatting(pdf_path)
    except Exception as e:
        printfail(provider,f"Error extracting formatted text: {e}")
        extracted_data['formatted_text'] = []

    # Extract fonts info
    try:
        if log:
            printinfo(provider,"Extracting fonts info...")
        extracted_data['fonts_info'] = extract_fonts_info(pdf_path)
    except Exception as e:
        printfail(provider,f"Error extracting fonts info: {e}")
        extracted_data['fonts_info'] = []

    # Extract links and annotations
    try:
        if log:
            printinfo(provider,"Extracting links and annotations...")
        extracted_data['links_and_annotations'] = extract_links_and_annotations(pdf_path)
    except Exception as e:
        printfail(provider,f"Error extracting links/annotations: {e}")
        extracted_data['links_and_annotations'] = []

    # WONTFIX
    # The extracted images is highly prone to getting fragmented so keeping a count of images is highly unreliable.
    # try:
    #     printinfo(provider,"Extracting IMGs...")
    #     doc = fitz.open(pdf_path)
    #     image_count = 0
    #     for page_num in range(doc.page_count):
    #         page = doc[page_num]
    #         image_list = page.get_images(full=True)
    #         image_count += len(image_list)
    #     doc.close()
    #     extracted_data['images'] = image_count
    # except Exception as e:
    #     printfail(provider,f"Error extracting IMGs: {e}")

    try:
        if log:
            printinfo(provider,"Extracting tables...")
        extracted_data['tables'] = extract_tables_from_pdf(pdf_path)
    except Exception as e:
        printfail(provider,f"Table extraction failed: {e}")
        extracted_data['tables'] = []

    return extracted_data

# Example usage
if __name__ == "__main__":
    # Replace with your PDF file path
    pdf_file = "paper.pdf"

    # Check if file exists
    if not Path(pdf_file).exists():
        print(f"Error: PDF file '{pdf_file}' not found!")
        exit(1)

    try:
        # Extract all data
        data = comprehensive_pdf_extraction(pdf_file)

        # Save extracted data to JSON
        output_file = "../extracted_pdf_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

        print(f"Extraction complete! Data saved to {output_file}")

        # Print summary
        print(f"\nExtraction Summary:")
        print(f"- Pages: {data['metadata']['page_count']}")
        print(f"- Text blocks extracted: {len(data['text_content'])}")
        print(f"- Images found: {len(data.get('images', []))}")
        print(f"- Tables found: {len(data.get('tables', []))}")
        print(f"- Links/Annotations: {len(data['links_and_annotations'])}")
        print(f"- Fonts used: {len(set(font['basefont'] for font in data['fonts_info']))}")

    except Exception as e:
        print(f"Error processing PDF: {e}")

# Individual extraction examples:

# 1. Extract just text
# text_data = extract_text_from_pdf("example.pdf")
# print(text_data[0]['text'])  # First page text

# 2. Extract just images
# images = extract_images_from_pdf("example.pdf")
# print(f"Found {len(images)} images")

# 3. Extract just metadata
# info = extract_metadata("example.pdf")
# print(f"Title: {info['metadata'].get('title', 'N/A')}")

# 4. Extract with specific formatting
# formatted = extract_text_with_formatting("example.pdf")
# for page in formatted:
#     print(f"Page {page['page']} has {len(page['blocks'])} text blocks")

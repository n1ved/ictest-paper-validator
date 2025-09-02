from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from app.utils.logger import printinfo, printsuccess, Logger

FONT_MAP = {
    'TimesNewRoman': 'Times-Roman',
    'Times New Roman': 'Times-Roman',
    'NimbusRoman': 'Times-Roman',
    'Nimbus Roman No9 L': 'Times-Roman',
    'Nimbus Rom No9 L': 'Times-Roman',
}
def map_font(font_name):
    return FONT_MAP.get(font_name.split(',')[0], 'Times-Roman')

def add_watermark(canvas_obj, text="Correction reference, not exact copy of submitted paper", opacity=0.5, font_size=30):
    width, height = A4
    canvas_obj.saveState()
    canvas_obj.setFont("Times-Roman", font_size)
    canvas_obj.setFillColorRGB(0.7, 0.7, 0.7, alpha=opacity)  # Light gray
    canvas_obj.translate(width / 2, height / 2)
    canvas_obj.rotate(45)
    canvas_obj.drawCentredString(0, 0, text)
    canvas_obj.restoreState()

def is_error_span(locator, error_locators):

    return any(
        locator['page'] == err['page'] and
        locator['block'] == err['block'] and
        locator['line'] == err['line'] and
        locator['span'] == err['span']
        for err in error_locators
    )

def render_pdf_from_extracted(extracted_data, output_path , error_spans=None):
    printinfo("PDF_RENDERER", f"Rendering PDF to {output_path}")
    c = canvas.Canvas(output_path, pagesize=A4)

    error_spans = error_spans or []
    printinfo("PDF_RENDERER", f"Number of error spans to highlight: {len(error_spans)}")
    print(error_spans)
    for page_idx, page in enumerate(extracted_data['formatted_text']):
        add_watermark(c)
        for block_idx,block in enumerate(page['blocks']):
            for line_idx,line in enumerate(block['lines']):
                for span_idx,span in enumerate(line['spans']):
                    text = span['text']
                    x, y = span['bbox'][0], span['bbox'][1]
                    font = map_font(span['font'])
                    size = span['size']
                    locator = {
                        'page': page_idx,
                        'block': block_idx,
                        'line': line_idx,
                        'span': span_idx
                    }
                    if is_error_span(locator, error_spans):
                        c.saveState()
                        c.setFillColorRGB(1, 0, 0)  # Red text
                        try:
                            c.setFont(font, size)
                        except Exception:
                            c.setFont('Times-Roman', size)
                        c.drawString(x, 800-y, text)
                        c.restoreState()
                    else:
                        c.setFont(font, size)
                        c.drawString(x, 800 - y, text)
        c.showPage()


    c.save()
    printsuccess("PDF_RENDERER", f"PDF rendering completed and saved to {output_path}")
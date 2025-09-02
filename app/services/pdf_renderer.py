from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from app.utils.logger import printinfo, printsuccess

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

def render_pdf_from_extracted(extracted_data, output_path):
    printinfo("PDF_RENDERER", f"Rendering PDF to {output_path}")
    c = canvas.Canvas(output_path, pagesize=A4)


    for page in extracted_data['formatted_text']:
        add_watermark(c)
        for block in page['blocks']:
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text']
                    x, y = span['bbox'][0], span['bbox'][1]
                    font = map_font(span['font'])
                    size = span['size']
                    color_r = (span['color'] >> 16) & 255
                    color_g = (span['color'] >> 8) & 255
                    color_b = span['color'] & 255
                    c.setFillColorRGB(color_r / 255, color_g / 255, color_b / 255)
                    c.setFont(font, size)
                    c.drawString(x, 800 - y, text)
        c.showPage()


    c.save()
    printsuccess("PDF_RENDERER", f"PDF rendering completed and saved to {output_path}")
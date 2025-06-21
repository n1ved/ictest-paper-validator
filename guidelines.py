# guidelines.py
"""
Central place for all format and validation rules.
Edit this file to update font, size, and style requirements for various sections.
"""
from logger import printfail


def check_font(family):
    newfamily = ''.join(family.split()).strip().lower()
    family_valid = False
    if(newfamily[:13] in font.lower() for font in GLOBAL_FONTS):
        family_valid = True
    else:
        printfail("FONT_VALIDATOR", f"Font {newfamily[:13]} is not a valid font family. Expected one of: {', '.join(GLOBAL_FONTS)}")
    return family_valid


# Global
GLOBAL_FONTS = ['TimesNewRoman' , 'Times New Roman' , 'NimbusRoman' , 'Nimbus Roman No9 L' , 'Nimbus Rom No9 L']
GLOBAL_FONTS_BOLD = [font + ',Bold' for font in GLOBAL_FONTS]
GLOBAL_FONTS_ITALIC = [font + ',Italic' for font in GLOBAL_FONTS]
GLOBAL_FONTS_BOLD_ITALIC = [font + ',BoldItalic' for font in GLOBAL_FONTS]

# Ignore some characters
GLOBAL_IGNORE_CHARS = ['\n', '\r', ' ', '', '—', '.', '–', '—', '“', '”', '‘', '’' ]

# PDFeXpress
GLOBAL_CREATOR_NAME = "Certified by IEEE PDFeXpress"
# Title rules
TITLE_FONT_FAMILIES = GLOBAL_FONTS
TITLE_FONT_SIZES = [24]
TITLE_FLAGS = [4]

# Abstract rules
ABSTRACT_FONT_FAMILIES = GLOBAL_FONTS_BOLD + GLOBAL_FONTS_BOLD_ITALIC
ABSTRACT_FONT_SIZES = [9]  # IEEE abstract is usually 10pt
ABSTRACT_FLAGS = [22, 20]

#TODO: Author rules
AUTHOR_FONT_FAMILIES = GLOBAL_FONTS
AUTHOR_FONT_SIZES = [10]
AUTHOR_BOLD = [False]
AUTHOR_ITALIC = [False]

# Keywords rules
KEYWORDS_FONT_FAMILIES = GLOBAL_FONTS_BOLD_ITALIC
KEYWORDS_FONT_SIZES = [9]
KEYWORDS_FLAGS = [22]

# Body text rules
BODY_FONT_FAMILIES = GLOBAL_FONTS
BODY_FONT_SIZES = [10]

# Page Margins
PAGE_SMALLEST_MARGIN = 64

#H1
H1_INDEX_FONT_SIZES = [10]
H1_INDEX_FLAGS = [4]
H1_FIRST_FONT_SIZES= [10]
H1_FIRST_FLAGS = [4]
H1_REST_FONT_SIZES = [8]
H1_REST_FLAGS = [4]


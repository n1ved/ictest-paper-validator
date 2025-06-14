# guidelines.py
"""
Central place for all format and validation rules.
Edit this file to update font, size, and style requirements for various sections.
"""

def check_font(family):
    newfamily = ''.join(family.split()).strip().lower()
    family_valid = False
    if(newfamily[:13] == GLOBAL_FONTS[0].lower()):
        family_valid = True
    return family_valid


# Global
GLOBAL_FONTS = ['TimesNewRoman' , 'Times New Roman']
GLOBAL_FONTS_BOLD = [font + ',Bold' for font in GLOBAL_FONTS]
GLOBAL_FONTS_ITALIC = [font + ',Italic' for font in GLOBAL_FONTS]
GLOBAL_FONTS_BOLD_ITALIC = [font + ',BoldItalic' for font in GLOBAL_FONTS]


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

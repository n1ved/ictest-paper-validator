# guidelines.py
"""
Central place for all format and validation rules.
Edit this file to update font, size, and style requirements for various sections.
"""

# Title rules
TITLE_FONT_FAMILIES = ['TimesNewRoman' , 'Times New Roman']
TITLE_FONT_SIZES = [24]
TITLE_FLAGS = [4]

# Abstract rules
ABSTRACT_FONT_FAMILIES = TITLE_FONT_FAMILIES
ABSTRACT_FONT_SIZES = [9]  # IEEE abstract is usually 10pt
ABSTRACT_FLAGS = [22, 20]

#TODO: Author rules
AUTHOR_FONT_FAMILIES = TITLE_FONT_FAMILIES
AUTHOR_FONT_SIZES = [10]
AUTHOR_BOLD = [False]
AUTHOR_ITALIC = [False]

# Keywords rules
KEYWORDS_FONT_FAMILIES = TITLE_FONT_FAMILIES
KEYWORDS_FONT_SIZES = [9]
KEYWORDS_FLAGS = [22]

# Body text rules
BODY_FONT_FAMILIES = TITLE_FONT_FAMILIES
BODY_FONT_SIZES = [10]

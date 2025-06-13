from guidelines import TITLE_FONT_FAMILIES
from guidelines import TITLE_FONT_SIZES
from guidelines import TITLE_FLAGS
import text_processor
def validate_title(title,log=False):
    '''
	pass the title to validate it
	currently checks
		- whether the title is in TimesNewRoman
		- whether the title is in 24pt font size
		- is neither bold nor italic
    '''
    processor = text_processor.quick_load('extracted_pdf_data.json')
    title_split = title.split()
    title_search = processor.search(title)
    breakp = 0
    for word in range(0,len(title_split)):
        prev_result = title_search
        strcated = ''
        for i in range(breakp , word):
            strcated += title_split[i] + ' '
        title_search = processor.search(strcated)
        if title_search.empty:
            if prev_result.empty:
                print('Error: Title text not found in document')
                return False

            font = prev_result['font'][0]
            font_size = prev_result['size'][0].round(0)
            flag = prev_result['flags'][0]
            if(font in TITLE_FONT_FAMILIES and font_size in TITLE_FONT_SIZES and flag in TITLE_FLAGS):
                if log:
                    print(strcated + ' -> ' + font)
                return True
            else:
                print('Error : FontError \n Invalid Font : ' + font + '@' + str(font_size) + 'pt')
                return False
            breakp = word

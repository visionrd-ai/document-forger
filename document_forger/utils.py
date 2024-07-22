import numpy as np
import pytesseract

DEFAULT_PROBABILITY = 0.2
TOTAL_DOCUMENTS = 1
CONFIDENCE_THRESHOLD = 80
DESKEW_IMAGE = False
MAX_TRIES = 10
FORMAT = 'png'

def set_tesseract_cmd(tesseract_cmd_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path
    
    
def check_format(img_format):
    if img_format not in ['png', 'jpeg', 'jpg']:
        return False
    return True
    
def get_max_top_bottom(characters):
    max_top = float('-inf')
    min_bottom = float('inf')
    for character in characters:
        max_top = max(max_top, character['top'])
        min_bottom = min(min_bottom, character['bottom'])
    #return min(max_top + 5, max_top), max(min_bottom - 5, 0)
    return max_top, min_bottom

def bounding_box_adjuster(characters):
    # return characters
    new_boxes = []
    max_top, min_bottom = get_max_top_bottom(characters)
    for i in range(len(characters)):
        character = characters[i]
        top = max(character['top'], max_top)
        bottom = min(character['bottom'], min_bottom)
        
        if i == 0:
            left = character['left']
        else:
            left = max(character['left'], characters[i - 1]['right'])

        if i == (len(characters) - 1):
            right = character['right']
        else:
            right = min(character['right'], characters[i + 1]['left'])
        
        new_boxes.append({
            'left': left,
            'top': top,
            'right': right,
            'bottom': bottom,
            'char': character['char']
        })
        
    return new_boxes

def get_character_index(text, characters):
    char_dict = {char['char']: i for i, char in enumerate(characters)}
    for i, start_char in enumerate(text):
        if start_char in char_dict:
            return char_dict[start_char]
    return -1

def compute_statistics(characters):
    widths = [char['right'] - char['left'] for char in characters]
    heights = [char['bottom'] - char['top'] for char in characters]
    tops = [char['top'] for char in characters]
    bottoms = [char['bottom'] for char in characters]

    stats = {
        'mean_width': np.mean(widths),
        'std_width': np.std(widths),
        'mean_height': np.mean(heights),
        'std_height': np.std(heights),
        'mean_top': np.mean(tops),
        'std_top': np.std(tops),
        'mean_bottom': np.mean(bottoms),
        'std_bottom': np.std(bottoms)
    }
    return stats
import numpy as np
import pytesseract

DEFAULT_PROBABILITY = 0.2
TOTAL_DOCUMENTS = 1
CONFIDENCE_THRESHOLD = 80
DESKEW_IMAGE = False
MAX_TRIES = 10

def set_tesseract_cmd(tesseract_cmd_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path

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
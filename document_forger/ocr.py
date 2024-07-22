import pytesseract
import pandas as pd
from tqdm import tqdm
from difflib import SequenceMatcher
from .utils import bounding_box_adjuster

def extract_words(img, annotations):
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    df = pd.DataFrame(data)
    df = df[df['text'].notna() & df['text'].str.len() > 0].reset_index(drop=True)
    for index, row in tqdm(df.iterrows(), desc='Extracting Words'):
        x, y, w, h = row['left'], row['top'], row['width'], row['height']
        text = row['text']
        annotations[str(index)] = {
            'left': x,
            'top': y,
            'width': w,
            'height': h,
            'text': text
        }
    return annotations

def extract_characters(img, annotations):
    new_annotations = {}
    for index, row in tqdm(annotations.items(), desc='Extracting Characters'):
        x, y, w, h = row['left'], row['top'], row['width'], row['height']
        text = row['text']
        new_annotations[f'{index}'] = {'text': text, 'characters': [], 'bbox': [x, y, w, h]}
        char_img = img[y:y+h, x:x+w]
        data = pytesseract.image_to_boxes(char_img, config='--psm 6', output_type=pytesseract.Output.DICT)
        df = pd.DataFrame(data)
        if df.empty: continue
        df = df[df['char'].notna() & df['char'].str.len() > 0].reset_index(drop=True)
        for _ , row1 in df.iterrows():
            x1, y1, r1, b1 = row1['left'], row1['top'], row1['right'], row1['bottom']
            text1 = row1['char']
            char_annotations = {
                'left': x1,
                'top': y1,
                'bottom': b1,
                'right': r1,
                'char': text1,
            }
            new_annotations[f'{index}']['characters'].append(char_annotations)
        new_annotations[f'{index}']['characters'] = bounding_box_adjuster(new_annotations[f'{index}']['characters'])
    return new_annotations

def image_comparison_string(img, text):
    img_text = pytesseract.image_to_string(img)
    similarity_ratio = SequenceMatcher(None, text, img_text).ratio()
    return similarity_ratio * 100

def image_comparison(img, text):
    img_text = pytesseract.image_to_boxes(img)
    lines = img_text.strip().split('\n')
    data = [dict(zip(['char', 'left', 'bottom', 'right', 'top'], line.split()[:5])) for line in lines]
    df = pd.DataFrame(data)
    if 'char' in df.columns:
        df = df[df['char'].notna() & df['char'].str.len() > 0].reset_index(drop=True)
        img_text = ''.join(df['char'])
        similarity_ratio = SequenceMatcher(None, text, img_text).ratio()
        return similarity_ratio * 100, img_text
    else:
        return None
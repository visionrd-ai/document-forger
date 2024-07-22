import os
import cv2
import json
import copy
import random
import numpy as np
import multiprocessing
from tqdm import tqdm
from time import time
from .utils import compute_statistics, check_format, get_character_index , DEFAULT_PROBABILITY, TOTAL_DOCUMENTS, CONFIDENCE_THRESHOLD, DESKEW_IMAGE, MAX_TRIES, FORMAT
from .ocr import extract_words, extract_characters, image_comparison
from .image_processing import process_image

def character_replacer(cv_img, text, characters, confidence_threshold, max_tries):
    index = get_character_index(text, characters)
    if index == -1:
        return None

    stats = compute_statistics(characters)
    temp_string = ''.join(char['char'] for char in characters)
    forged_img = copy.deepcopy(cv_img)

    for _ in range(max_tries):
        choice1 = random.randint(index, len(characters) - 1)
        choice2 = random.randint(index, len(characters) - 1)

        if choice1 == choice2:
            continue

        char1, char2 = characters[choice1], characters[choice2]
        
        if char1['char'].isupper() and char2['char'].islower() \
            or char1['char'].islower() and char2['char'].isupper():
            continue

        if char1['char'] == char2['char'] or char1['char'] == ' ' or char2['char'] == ' ':
            continue
        if len(char1['char']) != 1 or len(char2['char']) != 1:
            continue

        l1, t1, r1, b1 = char1['left'], char1['top'], char1['right'], char1['bottom']
        l2, t2, r2, b2 = char2['left'], char2['top'], char2['right'], char2['bottom']

        if abs(t1 - t2) <= stats['std_top'] and abs(b1 - b2) <= stats['std_bottom'] \
                and abs((r1 - l1) - (r2 - l2)) <= stats['std_width'] and abs((b1 - t1) - (b2 - t2)) <= stats['std_height']:
            new_width = abs(r1 - l1)
            new_height = abs(b1 - t1)
            if new_width > 0 and new_height > 0:
                resized_img = cv_img[b2:t2, l2:r2]
                try:
                    resized_img = cv2.resize(resized_img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
                except Exception as e:
                    return None
                
                forged_img[b1:t1, l1:r1] = resized_img
                temp_list = list(temp_string)
                temp_list[choice1] = char2['char']
                new_string = ''.join(temp_list)
                results = image_comparison(forged_img, new_string, text)
                if results is not None:
                    confidence , upd_str = results
                    if confidence >= confidence_threshold:
                        cv_img[b1:t1, l1:r1] = resized_img
                        return cv_img, text, upd_str
    return None

def process(i, cv_img, annotations, probability, confidence_threshold, output_dir, img_name, max_tries, img_format):
    forgeries_made = []
    duplicate_img = copy.deepcopy(cv_img)
    name = img_name.split('.')[0]
    for _ in range(max_tries):
        replacement_flag = False
        for _, row in annotations.items():
            if (random.random() < probability) or (len(row['characters']) <= 1):
                continue
            x, y, w, h = row['bbox']
            result = character_replacer(duplicate_img[y:y+h, x:x+w], row['text'], row['characters'], confidence_threshold, max_tries)
            if result is not None:
                img, text, modified_text = result
                duplicate_img[y:y+h, x:x+w] = img
                forgeries_made.append((text, modified_text))
                replacement_flag = True
        if replacement_flag:
            break
    cv2.imwrite(f'{output_dir}/{name}_{i}.{img_format}', duplicate_img)
    return forgeries_made, (f'{name}_{i}.{img_format}')

def process_document_wrapper(args):
    unique_seed = time() + os.getpid()
    random.seed(unique_seed)
    return process(*args)

def process_document(input_image, output_dir, probability=DEFAULT_PROBABILITY, total_documents=TOTAL_DOCUMENTS \
    , confidence_threshold=CONFIDENCE_THRESHOLD, deskew_image=DESKEW_IMAGE, max_tries=MAX_TRIES, img_format=FORMAT):
        
        if not check_format(img_format):
            raise ValueError('Invalid Output Image Format. Supported Formats are PNG, JPEG, JPG')

        if isinstance(input_image, np.ndarray):
            img_name = f'image.{img_format}'
        elif isinstance(input_image, str):
            if not os.path.exists(input_image):
                raise ValueError('Input Image does not exist.')
            img_name = os.path.basename(input_image)
            input_image_format = img_name.split('.')[-1]
            if not check_format(input_image_format):
                raise ValueError('Invalid Image Format. Supported Formats are PNG, JPEG, JPG')
        else:
            raise ValueError('Invalid Image Path or Image is not a Numpy Array')

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        annotations = {}
        pil_img, cv_img = process_image(input_image, deskew_image)
        annotations = extract_words(pil_img, annotations)
        annotations = extract_characters(cv_img, annotations)

        pool = multiprocessing.Pool(processes=(multiprocessing.cpu_count() // 2))
        args = [(i, cv_img, annotations, probability, confidence_threshold, output_dir, img_name, max_tries, img_format) for i in range(total_documents)]

        document_forgeries = {}
        for result in tqdm(pool.imap_unordered(process_document_wrapper, args), total=len(args), desc='Creating Documents'):
            forgeries_made, document_name = result
            document_forgeries[document_name] = forgeries_made

        with open(f'{output_dir}/document_forgeries.json', 'w') as f:
            json.dump(document_forgeries, f, indent=4)
            
        pool.close()
        pool.join()
        
        return document_forgeries

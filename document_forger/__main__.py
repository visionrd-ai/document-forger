import argparse
import os
from .document_processing import process_document
from .utils import set_tesseract_cmd, DEFAULT_PROBABILITY, TOTAL_DOCUMENTS, CONFIDENCE_THRESHOLD, DESKEW_IMAGE, MAX_TRIES

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Forging Documents')
    parser.add_argument('--image_path', type=str, required=True, help='Path to the image.')
    parser.add_argument('--probability', type=float, default=DEFAULT_PROBABILITY, help='Probability of character replacement.')
    parser.add_argument('--total_documents', type=int, default=TOTAL_DOCUMENTS, help='Total number of documents.')
    parser.add_argument('--output_dir', type=str, required=True, help='Output directory.')
    parser.add_argument('--confidence_threshold', type=int, default=CONFIDENCE_THRESHOLD, help='Threshold for confidence level.')
    parser.add_argument('--deskew_image', type=bool, default=DESKEW_IMAGE, help='Deskew the image or not.')
    parser.add_argument('--max_tries', type=int, default=MAX_TRIES, help='Maximum number of tries for character replacement at each word and document.')
    parser.add_argument('--tesseract_cmd', type=str, required=False, help='Path to Tesseract executable.')

    args = parser.parse_args()

    if not os.path.exists(args.image_path):
        print('Input image does not exist.')
        exit(1) 

    if not os.path.exists(args.output_dir):
        print('Invalid Path for Output Directory')
        exit(1)

    if args.tesseract_cmd:
        set_tesseract_cmd(args.tesseract_cmd)
        
    process_document(args.image_path, args.output_dir, args.probability, args.total_documents \
        , args.confidence_threshold, args.deskew_image, args.max_tries)

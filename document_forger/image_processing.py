import cv2
from PIL import Image
import numpy as np

def get_skew_angle(cv_image) -> float:
    new_image = cv_image.copy()
    gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)
    contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if len(contours) == 0:
        return 0.0
    largest_contour = contours[0]
    min_area_rect = cv2.minAreaRect(largest_contour)
    angle = min_area_rect[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = - angle
        if angle < -45:
            angle = (90 + angle)
    return angle

def rotate_image(cv_image, angle: float):
    (h, w) = cv_image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(cv_image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def deskew(cv_image, angle_threshold: float = 1.0):
    angle = get_skew_angle(cv_image)
    if abs(angle) > angle_threshold:
        return rotate_image(cv_image, -angle)
    return cv_image

def process_image(image_path, deskew_image):
    if isinstance(image_path, np.ndarray):
        cv_img = image_path
    elif isinstance(image_path, str):
        cv_img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    else:
        raise ValueError('Invalid Image Path or Image is not a Numpy Array')
    
    if cv_img is None:
        raise ValueError('Failed to Load Image')
    if deskew_image:
        cv_img = deskew(cv_img)
    gray_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    bin_img = cv2.threshold(gray_img, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    pil_img = Image.fromarray(bin_img)
    return pil_img, cv_img

def preprocess_image(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    pil_img = Image.fromarray(gray_img)
    return pil_img

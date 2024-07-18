import unittest
from document_forger.image_processing import get_skew_angle, rotate_image, deskew
import numpy as np

class TestTextProcessor(unittest.TestCase):

    def test_get_skew_angle(self):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        angle = get_skew_angle(img)
        self.assertIsInstance(angle, float)

    def test_rotate_image(self):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        rotated_img = rotate_image(img, 45)
        self.assertEqual(rotated_img.shape, img.shape)

    def test_deskew(self):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        deskewed_img = deskew(img)
        self.assertEqual(deskewed_img.shape, img.shape)

if __name__ == '__main__':
    unittest.main()

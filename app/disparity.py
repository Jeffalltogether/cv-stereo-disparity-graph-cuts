from scipy import ndimage
import cv2
import numpy as np

def to_gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
    return (gray - gray.mean()) / gray.std()

def convolve(image, kernel):
    return ndimage.filters.convolve(image, kernel, mode='constant', cval=0)

def disparity_ssd(image_left, image_right, kernel=7, max_search=30):
    gray_left = to_gray(image_left)
    gray_right = to_gray(image_right)
    kernel = np.ones((kernel, kernel), dtype=np.float32)

    height, width = gray_left.shape
    ssd = np.zeros((max_search, height, width), dtype=np.float32)
    for offset in range(max_search):
        shifted = gray_right if offset == 0 else gray_right[:, :-offset]
        ssd[offset, :, offset:] = np.square(gray_left[:, offset:] - shifted)
        ssd[offset] = convolve(ssd[offset], kernel)

    ssdmax = ssd.max()
    for offset in range(1, max_search):
        ssd[offset, :, :offset] = ssdmax

    return np.argmin(ssd, axis=0)
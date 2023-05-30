from PIL import ImageGrab
import numpy as np
import cv2
import time
from direct_keys import PressKey, ReleaseKey, W, A, S, D

# 4 seconds to switch to the game window
for i in list(range(4))[:: -1]:
    print(i + 1)
    time.sleep(1)

def process_img(original_image):
    # convert to gray from BGR
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img = cv2.Canny(processed_img, threshold1 = 200, threshold2 = 300)
    # return the processed image
    return processed_img
from PIL import ImageGrab
import numpy as np
import cv2
import time
from direct_keys import press_key, release_key, W, A, S, D

def process_img(original_image):
    # convert to gray from BGR
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img = cv2.Canny(processed_img, threshold1 = 200, threshold2 = 300)
    # return the processed image
    return processed_img

# 4 seconds to switch to the game window
for i in list(range(4))[:: -1]:
    print(i + 1)
    time.sleep(1)

last_time = time.time()
while(True):
    # 800 x 600 windowed mode
    screen = np.array(ImageGrab.grab(bbox = (0, 40, 800, 640)))
    new_screen = process_img(screen)

    # print loop that prints the time each print screen takes and prints to console
    print('loop took {} seconds'.format(time.time() - last_time))
    last_time = time.time()
    # displays the processed image
    cv2.imshow('window', new_screen)

    # if statement that breaks the loop if q is pressed for 25 milliseconds
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
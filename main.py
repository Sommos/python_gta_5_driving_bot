from PIL import ImageGrab
import numpy as np
import cv2
import time

# sets the time at the start of the program
last_time = time.time()
while(True):
    # 800 x 600 windowed mode
    screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
    
    # print loop that prints the time each print screen takes and prints to console
    print('loop took {} seconds'.format(time.time() - last_time))
    last_time = time.time()

    # displays the image. and converts printscreen_pil to a numpy array from a PIL image
    cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))

    # if statement that breaks the loop if q is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
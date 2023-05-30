from PIL import ImageGrab
from direct_keys import press_key, release_key, W, A, S, D
import numpy as np
import cv2
import time

def region_of_interest(img, vertices):
    # blank mask
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    # return the masked image
    return masked

def draw_lines(img, lines):
    try:
        for line in lines:
            # convert the line to a 2D array
            coords = line[0]
            # draw the line on the image with white color and thickness of 3
            cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 255], 3)
    except:
        pass

def process_img(original_image):
    # convert to gray from BGR
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img = cv2.Canny(processed_img, threshold1 = 200, threshold2 = 300)
    # gaussian blur the image
    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
    # vertices of the polygon
    vertices = np.array([
                        [10, 500], 
                        [10, 300], 
                        [300, 200], 
                        [500, 200], 
                        [800, 300], 
                        [800, 500]
                        ])
    # call the region of interest function over the processed image
    processed_img = region_of_interest(processed_img, [vertices])
    # call the HoughLinesP function over the processed image
    # cv2.HoughLinesP(image, rho, thetha, threshold, lines, minLineLength, maxLineGap)
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, 20, 15)
    # call the draw_lines function over the processed image
    draw_lines(processed_img, lines)
    # return the processed image
    return processed_img

def main():
    last_time = time.time()
    while(True):
        # 800 x 600 windowed mode
        screen = np.array(ImageGrab.grab(bbox = (0, 40, 800, 640)))
        new_screen = process_img(screen)

        # print loop that prints the time each print screen takes and prints to console
        print('Loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()
        # displays the processed image
        cv2.imshow('window', new_screen)

        # if statement that breaks the loop if q is pressed for 25 milliseconds
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()
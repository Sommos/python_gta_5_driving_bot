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

def draw_lanes(img, lines, color = [0, 255, 255], thickness = 3):
    try:
        # create an empty array to store y-coordinates of lines
        ys = []
        # loop through all the lines and store y-coordinates in the array
        for i in lines:
            for ii in i:
                ys += [ii[1], ii[3]]
        # find the min and max y-coordinates
        min_y = min(ys)
        max_y = 600
        # create an empty array to store slope and intercept of lines
        new_lines = []
        line_dict = {}

        # loop through all the lines and find slope, intercept and coordinates of lines and add them to the arrays
        for idx, i in enumerate(lines):
            for n in i:
                # find the slope and intercept of the lines
                x_coords = (n[0], n[2])
                y_coords = (n[1], n[3])
                # stacks the array vertically
                A = np.vstack([x_coords, np.ones(len(x_coords))]).T
                # find the slope and intercept
                slope, y_intercept = np.linalg.lstsq(A, y_coords)[0]
                # find the coordinates of the lines
                x1 = (min_y - y_intercept) / slope
                x2 = (max_y - y_intercept) / slope
                # add the slope, intercept and coordinates of the lines to the array
                line_dict[idx] = [slope, y_intercept, [int(x1), min_y, int(x2), max_y]]
                # add the coordinates of the lines to the array
                new_lines.append([int(x1), min_y, int(x2), max_y])
        
        # create an empty array to store slope and intercept of lines
        final_lanes = {}

        # loop through all the lines and find slope, intercept and coordinates of lines and add them to the arrays    
        for idx in line_dict:
            # create a copy of the final_lanes array
            final_lanes_copy = final_lanes.copy()
            # store the slope
            slope = line_dict[idx][0]
            # store the intercept
            y_intercept = line_dict[idx][1]
            # store the coordinates of the lines
            line = line_dict[idx][2]

            # if the final_lanes array is empty, add the slope, intercept and coordinates of the lines to the array
            if len(final_lanes) == 0:
                final_lanes[slope] = [[slope, y_intercept, line]]
            else:
                found_copy = False
                # loop through all the slopes in the final_lanes array
                for other_ms in final_lanes_copy:
                    # if the slope is similar to the slope in the final_lanes array, add the slope, intercept and coordinates of the lines to the array
                    if not found_copy:
                        if abs(other_ms * 1.2) > abs(slope) > abs(other_ms * 0.8):
                            if abs(final_lanes_copy[other_ms][0][1] * 1.2) > abs(y_intercept) > abs(final_lanes_copy[other_ms][0][1] * 0.8):
                                final_lanes[other_ms].append([slope, y_intercept, line])
                                found_copy = True
                                break
                        else:
                            # if the slope is not similar to the slope in the final_lanes array, add the slope, intercept and coordinates of the lines to the array
                            final_lanes[slope] = [[slope, y_intercept, line]]
        
        # create an empty array to store the coordinates of the lines
        line_counter = {}
        # loop through all the slopes in the final_lanes array and find the coordinates of the lines
        for lanes in final_lanes:
            line_counter[lanes] = len(final_lanes[lanes])
        # sort the lines in the final_lanes array based on the number of lines
        top_lanes = sorted(line_counter.items(), key = lambda item: item[1])[::-1][:2]
        # loop through all the top lines and draw the lines on the image
        lane1_id = top_lanes[0][0]
        lane2_id = top_lanes[1][0]

        # find the average coordinates of the lines
        def average_lane(lane_data):
            # create empty arrays to store the coordinates of the lines
            x1s = []
            y1s = []
            x2s = []
            y2s = []
            # loop through all the data and append to the arrays
            for data in lane_data:
                x1s.append(data[2][0])
                y1s.append(data[2][1])
                x2s.append(data[2][2])
                y2s.append(data[2][3])
            # find the average of the coordinates, and convert them to integers before returning
            return int(np.mean(x1s)), int(np.mean(y1s)), int(np.mean(x2s)), int(np.mean(y2s))
        
        # find the average coordinates of the lines, and save them in the variables
        l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

        # draw the lines on the image
        return [[l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2]]
    # if no lines are detected, return the error message
    except Exception as e:
        print(str(e))

def process_img(image):
    # save a copy of the original image
    original_image = image
    # convert to gray from BGR
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img = cv2.Canny(processed_img, threshold1 = 200, threshold2 = 300)
    # # gaussian blur the image
    # processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
    # vertices of the polygon
    vertices = np.array([
                        [10, 500], 
                        [10, 300], 
                        [300, 200], 
                        [500, 200], 
                        [800, 300], 
                        [800, 500],
                        ], np.int32)
    # call the region of interest function over the processed image
    processed_img = region_of_interest(processed_img, [vertices])
    # call the HoughLinesP function over the processed image
    # cv2.HoughLinesP(image, rho, thetha, threshold, lines, minLineLength, maxLineGap)
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]), 20, 15)
    try:
        # call the draw_lanes function over the original image
        l1, l2 = draw_lanes(original_image, lines)
        # draw the lines on the original image
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0, 255, 0], 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0, 255, 0], 30)
    # if no lines are detected, return the error message
    except Exception as e:
        print(str(e))
        pass
    
    try:
        for coords in lines:
            coords = coords[0]
            try:
                # draw the lines on the processed image in blue
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 0, 0], 3)
            # if no lines are detected, return the error message
            except Exception as e:
                print(str(e))
    except Exception as e:
        pass
    # return the processed image and the original image
    return processed_img, original_image

def main():
    last_time = time.time()
    while(True):
        # 800 x 600 windowed mode
        screen = np.array(ImageGrab.grab(bbox = (0, 40, 800, 640)))
        # print loop that prints the time each print screen takes and prints to console
        print('Loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()
        new_screen, original_image = process_img(screen)
        # displays the processed image
        cv2.imshow('window', new_screen)
        # displays the original image
        cv2.imshow('window2', cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))

        # if statement that breaks the loop if q is pressed for 25 milliseconds
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()
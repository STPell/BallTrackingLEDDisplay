"""
   end_deliverable.py
   A program to track a ball via a camera.
   Author: Samuel Pell
   Date: 29-08-18 (DD-MM-YY)

   Created for an ENEL300 Group Design and Build Project: Group O

   Tracks the postion of a ball using the openCV library. The speed, angle, and
   position are then reported overal serial to a connected Arduino.
"""

from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import math
import SerialController
import statistics

#detection bounds for colour of the ball
GREEN_LOWER = (29, 86, 6)
GREEN_UPPER = (64, 255, 255)

TEXT_OUTPUT = "x={}, y={}, v={}, theta={}, delay={}"
AVERAGE_DELAY_OUTPUT = "Average delay of {} ms"

MATRIX_SIZE_X = 12
MATRIX_SIZE_Y = 12

FRAME_W = 600
FRAME_H = 600

W_PORT = 'COM3' #port arduino is on in windows
U_PORT = '/dev/ttyUSB0' #port test devices is on in ubuntu

def input_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", default=False, help="path to the (optional) video file")
    ap.add_argument("-s", "--serial", default=False, help="use serial output")
    ap.add_argument("-pc", "--print_calculus", default=False, help="print calculus info to console")
    ap.add_argument("-c", "--camera", type=int, default=0, help="camera to use for input")
    ap.add_argument("-d", "--display", default=False, help="display video overlay")
    return vars(ap.parse_args())


def average(delays):
    if len(delays) != 0:
        ave = sum(delays)/len(delays)
        return round(ave*1000, 2)
    else:
        return 0


def get_frame(stream, is_pre_captured):
    """Get a frame from the input stream, if needs be extract the frame data"""
    frame = stream.read()
    if is_pre_captured:
        return frame[1]
    else:
        return frame


def apply_mask(frame):
    """Apply a mask to the frame to isolate the colour of the object"""
    # resize blur it, and convert fame to the HSV
    #frame = imutils.resize(frame, width=FRAME_W, height=FRAME_H)
    frame = cv2.resize(frame, (FRAME_W, FRAME_H), interpolation=3)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    #mask colour out and clean up the mask
    mask = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    return frame, mask


def find_contours(masked_frame):
    # find contours in the mask
    contours = cv2.findContours(masked_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if imutils.is_cv2():
        return contours[0]
    else:
        return contours[1]


def find_min_circle(contours):
    """
       Find the CoM and the min enclosing circle from the
       contours of the object
    """
    center = (0, 0)
    radius = 0

    if len(contours) > 0:
    #compute the minimum enclosing circle and centroid
        c = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    else:
        #ball not found
        center = None
        radius = None
    return center, radius


def overlay_position(frame, centre, radius):
    """Show an enclosing circle and the CoM of the ball"""
    if (not (radius is None)) and radius > 10:
        cv2.circle(frame, centre, int(radius),(0, 255, 255), 2)
        cv2.circle(frame, centre, 5, (0, 0, 255), -1)
    return frame


def calculate_angle(centre, prev_centre):
    """Calculate the realative angle of travel between time steps"""
    o = centre[1] - prev_centre[1]
    a = centre[0] - prev_centre[0]
    return round(math.degrees(math.atan2(o, a)))


def calculate_speed(centre, prev_centre, time_step):
    """Calculate the speed of the CoM in pixels per second"""
    if time_step != 0:
        y = centre[1] - prev_centre[1]
        x = centre[0] - prev_centre[0]
        return round(math.hypot(x, y) / (time_step * FRAME_W), 2)
    else:
        return 0


def map_to_matrix(x, y):
    """maps pixel values to LED matrix index (starting from 0)"""
    x_pos = round(x * ((MATRIX_SIZE_X - 1)/(FRAME_W - 1)))
    y_pos = round(y * ((MATRIX_SIZE_Y - 1)/(FRAME_H - 1)))
    return x_pos, y_pos


def add_grid(img):
    """Adds a grid corresponding to which LED should be on in the matrix"""
    for i in range(1, MATRIX_SIZE_X):
        x_pos = int(round(i * FRAME_W / MATRIX_SIZE_X, 0))
        cv2.line(img, (x_pos, 0), (x_pos, FRAME_H), (0, 0, 255))

    for i in range(1, MATRIX_SIZE_Y):
        y_pos = int(round(i * FRAME_H / MATRIX_SIZE_Y, 0))
        cv2.line(img, (0, y_pos), (FRAME_W, y_pos), (0, 0, 255))

    return img


def display_frame(frame):
    cv2.imshow("Frame", frame)


def main_loop(args):
    centre = (0, 0)
    angle = 0
    speed = 0
    delays = []


    if args["video"]:
        vs = cv2.VideoCapture(args["video"])
    else:
        vs = VideoStream(src=args["camera"]).start()

    if args["serial"]:
        serial_port = SerialController.SerialController(U_PORT)
        serial_port.open_serial()

    time.sleep(5.0) #5 s delay to let things catch up

    done = False
    curr_time = time.time()
    while not done:
        prev_centre, prev_angle, prev_time = centre, angle, curr_time
        frame = get_frame(vs, args["video"])
        curr_time = time.time()

        if frame is None:
            #if there is nothing left to process
            done = True
        else:
            frame, masked_frame = apply_mask(frame)
            contour_list = find_contours(masked_frame)
            centre, radius = find_min_circle(contour_list)

            if centre is None:
                # if tracker not found
                x_pos, y_pos, speed, angle = -1, -1, 0, 0
                prev_centre = 0,0
                centre = 0,0
            else:
                x_pos, y_pos = map_to_matrix(*centre)
                speed = calculate_speed(centre, prev_centre, curr_time - prev_time)
                angle = calculate_angle(centre, prev_centre)

            if args["print_calculus"]:
                #print(TEXT_OUTPUT.format(*centre, speed, angle, curr_time - prev_time));
                print(TEXT_OUTPUT.format(x_pos, y_pos, speed, angle, curr_time - prev_time));
                delays.append(curr_time - prev_time)

            if args["display"]:
                display_frame(add_grid(overlay_position(frame, centre, radius)))
                key = cv2.waitKey(1) & 0xFF #Wait for ~1 ms to display image
                if key == ord('q'):
                    print("exiting on command")
                    done = True

            if args["serial"]:
                serial_port.write_data([x_pos, y_pos, speed, angle])


    if args["video"]:
        vs.release()
    else:
        vs.stop()
    cv2.destroyAllWindows()

    if args["serial"]:
        serial_port.close_serial()

    if args["print_calculus"]:
        print(AVERAGE_DELAY_OUTPUT.format(average(delays)))

if __name__ == "__main__":
    args = input_args();
    main_loop(args)


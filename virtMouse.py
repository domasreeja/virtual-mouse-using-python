from turtle import ht
import cv2  # pip install opencv-contrib-python
import numpy as np
import mediapipe as mp  # pip install mediapipe
import pyautogui    # pip install PyautoGUI
import matplotlib.pyplot as plt
#from IPython.display import Image

cap = cv2.VideoCapture(0)   # capture video '0' one cam
hand_detector = mp.solutions.hands.Hands()  # detect hand
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

'''Smoothen the movement of mouse to stop at the exact position of,
our hand movement without any shake in the movement of the mouse'''
smoothening = 9
plocx, plocy = 0, 0
clocx, clocy = 0, 0

while True:
    _,frame = cap.read()   # read data from cap
    frame = cv2.flip(frame, 1)
 
# shape gives frame height and width using shape
frame_height, frame_width, _ = frame.shape
rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # detect on rgb frame color
output = hand_detector.process(rgb_frame)
hands = output. multi_hand_landmarks # hand landmark

if hands:
    for hand in hands:
        drawing_utils.draw_landmarks(frame, hand)   # see landmarks on frame
        landmarks = hand. landmark
        for id, landmark in enumerate(landmarks):   # add counter
            x = int(landmark.x*frame_width)
            y = int(landmark.y*frame_height)
            landmarks = hand.landmark
            if id == 8:
                cv2.circle(img=frame, center=(x,y), radius=15, color=(0, 255, 255))
                index_x = (screen_width/frame_width)*x
                index_y = (screen_height/frame_height)*y
                clocx = plocx + (index_x - plocx) /smoothening
                clocy = plocy + (index_y - plocy) /smoothening
                pyautogui.moveTo(clocx, clocy)
                plocx, plocy = clocx, clocy
            if id == 4:
                cv2.circle(img=frame, center=(x,y), radius=15, color=(0, 255, 255))
                thumb_x = (screen_width/frame_width)*x
                thumb_y = (screen_height/frame_height)*y
                print('distance : ', abs(index_y - thumb_y))
                if abs(index_y - thumb_y) < 70:
                    print('click')
                    pyautogui.click()
                    pyautogui.sleep(1)
                    cv2.imshow('Virtual Mouse', frame)  # show image
                    cv2.waitKey(1)  # waits for key infinitely




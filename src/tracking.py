# tracking.py
# Created by Michael Marek (2016)
# Track the position of tennis balls in a webcam video feed.

import cv2
import numpy as np

capture = cv2.VideoCapture(0)

while(True):
    grabbed, frame = capture.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if not grabbed:
        break

    # tennis ball colour range
    lower = (29, 86, 6)
    upper = (64, 255, 255)

    # you can also track, uhh, lemons with this colour range
    # lower = (10, 100, 100)
    # upper = (40, 255, 255)

    mask = cv2.inRange(hsv, lower, upper)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # mask = cv2.GaussianBlur(mask, (3, 3), 2)

    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        if radius > 10:
            cv2.circle(frame, center, radius, (0, 255, 0), 2) # tennis ball outline
            cv2.circle(frame, center, 1, (0, 0, 255), 2)      # tennis ball centroid

    cv2.imshow('Tennis Ball Tracking', frame)

    if cv2.waitKey(30) & 0xFF == 27:
        break

capture.release()
cv2.destroyAllWindows()

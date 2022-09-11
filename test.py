import cv2
import numpy as np
from matplotlib import pyplot as plt

def union(a,b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0]+a[2], b[0]+b[2]) - x
    h = max(a[1]+a[3], b[1]+b[3]) - y
    return (x, y, w, h)


# reading image
img = cv2.imread('mazes/maze.png')
img = cv2.resize(img, (0, 0), fx=0.8, fy=0.8)

# img = cv2.GaussianBlur(img, (9, 9), 0)
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# setting threshold of gray image
_, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
cv2.imshow("window", threshold)
cv2.waitKey(0)

# using a findContours() function
contours, _ = cv2.findContours(
    threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cnt = sorted(contours, key=cv2.contourArea, reverse=True)
cnt = cnt[1:]

for contour in cnt:
    tmp = cv2.drawContours(img.copy(), [contour], 0, (0, 0, 255), 5)
    cv2.imshow("window", tmp)
    print(cv2.contourArea(contour))
    cv2.waitKey(0)


cv2.imshow('shapes', img)
cv2.imwrite("contours.png", img)

cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2 as cv
import pickle
import cvzone
import numpy as np


#Video feed ->>
cap = cv.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48

def checkParkingSpace(imgPro):

    spaceCounter = 0

    for pos in posList:
        x,y = pos

        imgCrop = imgPro[y:y+height, x:x+width]
        # cv.imshow(str(x*y), imgCrop)
        count = cv.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y+height -3), scale = 1, thickness=2, offset=0)
        if count < 900:
            color = (0,255,0)
            thickness = 3
            spaceCounter+=1
        else:
            color = (0,0,255)
            thickness = 2

        cv.rectangle(img, pos, (pos[0] + width, pos[1] + height), color=color, thickness=thickness)

    cvzone.putTextRect(img, f'Free {spaceCounter}/{len(posList)}', (100, 50), scale = 3, thickness=4, offset=20, colorR=(0,200,0))

while True:

    if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv.medianBlur(imgThreshold, 5)
    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)

    cv.imshow('Image', img)
    # cv.imshow('GrayImage', imgGray)
    # cv.imshow('BlurImage', imgBlur)
    # # cv.imshow('ThresHold', imgThreshold)
    # cv.imshow('Median', imgMedian)

    key = cv.waitKey(10)
    if key == 27:
        break

cv.destroyAllWindows()
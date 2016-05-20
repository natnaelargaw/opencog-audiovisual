__author__ = 'natnael'
import cv2
import numpy



def Visibility(data, row, col):
    sum1=0
    for i in range(row):
        for j in range(col):
            sum1 = sum1 + data[i][j]
    sum1 = sum1/((row*col))
    if sum1 < 50:
        return 'Dark' + ' '+str(sum1)
    elif sum1 < 95:
        return 'Light Dark' + ' '+str(sum1)
    elif sum1 < 120:
        return 'Minima' + ' '+str(sum1)
    elif sum1 < 165:
        return 'Normal' + ' '+str(sum1)
    else:
        return 'Bright' + ' '+str(sum1)

def entry():
    video_capture = cv2.VideoCapture(0)
import cv2
__author__ = 'ati'
import cv
import numpy
# What is left: black and white wear affects the decision
# Try: HSV light extraction
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

    flag = 0
    counter=1
    sum = 0
    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = frame.shape[:2]
        gray2 = gray[0:h,0:w/2] # 0:480 row and 0:320 column
        gray3 = gray[0:h, w/2:w]

        # if not counter % 25:
            # print(Visibility(gray, h, w))
            # cv2.imshow('Left', gray2)
            # cv2.imshow('Right', gray3)
            # print('Left: '+ str(Visibility(gray2,h, w/2)))
            # print('Right: '+ str(Visibility(gray3,h, w/2)))
        counter =counter + 1
        cv2.putText(frame,(Visibility(gray, h, w)),(w/2-70,30), font, 0.5,(255,255,255),2)
        cv2.putText(frame,(Visibility(gray2,h, w/2)),(10,h/2), font, 0.5,(255,255,255),2)
        cv2.putText(frame,(Visibility(gray3,h, w/2)),(w-100,h/2), font, 0.5,(255,255,255),2)
        cv2.imshow('VIDEO', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    font = cv2.FONT_HERSHEY_SIMPLEX
    entry()
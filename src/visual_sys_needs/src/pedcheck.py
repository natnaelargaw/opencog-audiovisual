# import the necessary packages
import datetime
import time
import cv2

def logTargetData():


    return True


def compareTargets():


    return True




def entry():
    pre=0
    firstFrame = None
    StartTime = time.time()
    # camera = cv2.VideoCapture('/home/natnael/sample.webm')
    camera = cv2.VideoCapture(0)
    counter=1
    while True:
        # Get the current frame
        ret, frame = camera.read()
        a= int(counter%140) #
        # cv2.imshow("Difference", frame[0:0, 100:100])#  frame[0 -(starting x.y):150-(height), 0:300-(width)]
        for i in range(65):
            cv2.imshow("Crop Feed", frame[a:a+200, 0:100])
            MajorQueue.append(frame[a:a+200, 0:100])
            cv2.imshow("Crop Feed", MajorQueue[0])

            # print(queue[0])
            cv2.rectangle(frame, (0+i*10, a), (150, a + 200+10), (255, 255, 255), 2)
            cv2.rectangle(frame, (0+i*10, a+140), (150, a+140 + 200+10), (255, 255, 255), 2)

        MajorQueue.clear()
        cv2.imshow("Security Feed", frame)

        print(a)
        counter = counter +1

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
   global MajorQueue
   MajorQueue = []
   entry()
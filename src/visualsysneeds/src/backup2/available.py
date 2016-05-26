# import the necessary packages
import datetime
import time
import cv2
from collections import deque
trend = ''
def maxOfSome(statetrend):
    ref = 0
    for i in statetrend:
        if i > ref:
            ref = i
    return ref

def dequeImp(count, currentState):
    if count < frameConstant:# In case of 42, around 4s queue accumulation time
        d.append(currentState)
        return d
    else:
        d.popleft()
        d.append(currentState)
        return d

#Every thing starts here
def entry():
    pre=0
    firstFrame = None
    StartTime = time.time()
    camera = cv2.VideoCapture(0)
    counter=1
    while True:
        # Get the current frame
        ret, frame = camera.read()
        Data = 0

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Initializing the First Reference Frame
        if firstFrame is None:
            firstFrame = gray
            continue

        # Subtracting the current frame from the reference Frame and converting it to Binary img based on the threshold
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        #Dilating the Image to fill merge tiny white areas.Also one can use erode to discover only large objects/moves.
        thresh = cv2.dilate(thresh, None, iterations=10)


        # find contours w. greater area;> cntArea
        (_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # discard the first _, if it raise error
        activeSub=0 # number of moving objects
        for c in cnts:
            if cv2.contourArea(c) < cntArea:
                continue
            activeSub = activeSub + 1
            (x, y, w, h) = cv2.boundingRect(c)
            print(x,y,w,h)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

        # Counting Active Locomotives
        state = 0
        if activeSub >= 0:
            state = int(activeSub * 0.75) # the more person exist the more impact
        else:
            state= -1
        Data=activeSub

        #Only for Demoing purpose
        cv2.putText(frame, "Targets on Move: {}".format(Data), (10, 15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "Peoples Seen: {}".format(maxOfSome(dequeImp(counter,activeSub))), (450, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        counter =counter + 1

        # cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        # (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

        # Frame Sampling: Once in every 3 seconds
        x= int(abs(time.time() - StartTime))
        if not x % TimeConstant:
            if x != pre:
                pre = x
                firstFrame = gray
        cv2.imshow("Security Feed", frame)

        cv2.imshow("Thresh", thresh)
        # cv2.imshow("Frame Delta", frameDelta)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    global firstFrame, Data, pre, d, frameConstant, cntArea, TimeConstant, ref
    # change this val to alter
    ref= 0
    TimeConstant=3  # 1. frame sampling rate
    frameConstant= 168# 3. Trend decision KB
    d= deque()
    trend= ''
    entry()

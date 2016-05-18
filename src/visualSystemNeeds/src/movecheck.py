# import the necessary packages
import datetime
import time
import cv2
from collections import deque
trend=''

'''shall be managed in a way it can subscribe to distance Mat and decide the impact of move based on the distance
the greater distance the higher dilation and the nearer distance the higher erosion iteration  '''
def getROIdistance():
    return True

#To be changed by Neural Net Classifier
def choasIdentifier(trend1):
    sumOf=0
    for i in trend1:
        sumOf= sumOf + i
    print(sumOf)
    if sumOf > (frameConstant-7):                   return 'Chaotic'
    elif sumOf < (-1 * frameConstant+7):          return 'Placid'
    else:                                         return 'Normal'

def dequeImp(count, currentState):
    if count < frameConstant:# In case of 42, around 4s queue accumulation time
        d.append(currentState)
        trend = 'Initializing'
        return trend
    else:
        d.popleft()
        d.append(currentState)
        trend = choasIdentifier(d)
        return trend

#Every thing starts here
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
        Data = 0

        #Frame: Convert it To Gray and apply Gaussian blur
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
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        activeSub=0 # number of moving objects
        for c in cnts:
            if cv2.contourArea(c) < cntArea:
                continue
            activeSub = activeSub + 1
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
        # Counting Active Locomotives
        state = 0
        if activeSub >= 1:
            state = 1
        else:
            state= -1
        Data=activeSub

        # Get the state of the room in the past (frameConstant/10) seconds
        trend = dequeImp(counter,state)
        counter =counter + 1

        #Only for Demoing purpose
        cv2.putText(frame, "Targets on Move: {}".format(Data), (10, 15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "Trend: {}".format(trend), (450, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        # (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

        # Frame Sampling: Once in every 3 seconds
        x= int(abs(time.time() - StartTime))
        if not x % TimeConstant:
            if x != pre:
                pre = x
                firstFrame = gray
        cv2.imshow("Security Feed", frame)

        # cv2.imshow("Thresh", thresh)
        # cv2.imshow("Frame Delta", frameDelta)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    global firstFrame, Data, pre, d, frameConstant, cntArea, TimeConstant
    # change this val to alter
    TimeConstant=3  # 1. frame sampling rate
    cntArea=15000   # 2. impact of small changes
    frameConstant= 42# 3. Trend decision KB
    d= deque()
    trend= ''
    entry()
#!/usr/bin/env python
from __future__ import print_function
from collections import deque
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import roslib
import sys
import rospy
import cv2
import time

roslib.load_manifest('visualsysneeds')

class RoomSilence:

  def __init__(self):
    self.counter = 1
    self.firstFrame = None
    self.pub2 = rospy.Publisher('/opencog/roomoccupation', String, queue_size=30)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/usb_cam_node/image_raw",Image, self.callback)

  def maxOfSome(self, statetrend):
    ref = 0
    for i in statetrend:
        if i > ref:
            ref = i
    return ref

  def dequeImp(self, count, currentState):
    if count < frameConstant:# In case of 42, around 4s queue accumulation time
        d.append(currentState)
        return d
    else:
        d.popleft()
        d.append(currentState)
        return d


  def callback(self,data):
    try:
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        #Frame: Convert it To Gray and apply Gaussian blur
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Initializing the First Reference Frame
        if self.firstFrame is None:
            self.firstFrame = gray
        # Subtracting the current frame from the reference Frame and converting it to Binary img based on the threshold
        frameDelta = cv2.absdiff(self.firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        #Dilating the Image to fill merge tiny white areas.Also one can use erode to discover only large objects/moves.
        thresh = cv2.dilate(thresh, None, iterations=10)
        # find contours w. greater area;> cntArea
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)# discard/add the prefix _, before cnts, if it raise error
        activeSub=0 # number of moving objects
        for c in cnts:
            if cv2.contourArea(c) < cntArea:
                continue
            activeSub = activeSub + 1
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(cv_image, (x, y), (x + w, y + h), (255, 255, 255), 2)
        # Counting Active Locomotion
        state = 0
        if activeSub >= 0:
            state = int(activeSub * 0.75) # the more person exist the more impact
        else:
            state= -1
        Data = str(activeSub)
        # Get the state of the room in the past (frameConstant/10) seconds
        # trend = self.roomsilence(self.counter,state)
        self.counter = self.counter + 1
        self.pub2.publish(str(self.maxOfSome(self.dequeImp(self.counter,activeSub))))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit(0)
    except CvBridgeError as e:
        print(e)



def main(args):
    global frameConstant
    global d
    global StartTime
    global pre
    global firstFrame
    global cntArea
    cntArea=15000
    d= d= deque()
    frameConstant = 42
    pre=0
    firstFrame = None
    StartTime = time.time()

    RoomSilence()
    rospy.init_node('RoomOccupation', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
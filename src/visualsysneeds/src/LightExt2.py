#!/usr/bin/env python
from __future__ import print_function
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import roslib
import sys
import rospy
import cv2

roslib.load_manifest('visualsysneeds')

class light_dark_classifier:
    def __init__(self):
        # self.image_pub = rospy.Publisher("image_topic_2",Image)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam_node/image_raw",Image,self.callback)# tobe changed by the chest-cam topic

    def __init__(self):
        self.roomInt = rospy.Publisher("/opencog/roomlight",Image)
        self.bridge = CvBridge()
        self.getimg = rospy.Subscriber("/usb_cam_node/image_raw",Image,self.imgcallback)# tobe changed by the chest-cam topic

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


    def imgcallback(self,data):

        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            h, w = cv_image.shape[:2]
            gray2 = gray[0:h,0:w/2] # 0:480 row and 0:320 column
            gray3 = gray[0:h, w/2:w]
            counter = counter + 1
        except CvBridgeError as e:
          print(e)

        (rows,cols,channels) = cv_image.shape
        if cols > 60 and rows > 60 :
          cv2.circle(cv_image, (50,50), 10, 255)

        cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)

















        counter=1
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            h, w = cv_image.shape[:2]
            gray2 = gray[0:h,0:w/2] # 0:480 row and 0:320 column
            gray3 = gray[0:h, w/2:w]
            counter =counter + 1
            cv2.putText(cv_image,(self.Visibility(gray, h, w)),(320-70,30), font, 0.5,(255,255,255),2)
            cv2.putText(cv_image,(self.Visibility(gray2,h, 320)),(10,240), font, 0.5,(255,255,255),2)
            cv2.putText(cv_image,(self.Visibility(gray3,h, 320)),(w-100,240), font, 0.5,(255,255,255),2)
            cv2.imshow('VIDEO', cv_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit(0)


        except CvBridgeError as e:
            print(e)
        (rows,cols,channels) = cv_image.shape
        if cols > 60 and rows > 60 :
            cv2.circle(cv_image, (50,50), 10, 255)

        cv2.imshow("RoomLight", cv_image)
        cv2.waitKey(3)


        # try:
        #   self.roomInt.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        # except CvBridgeError as e:
        #   print(e)
        #

    def main(args):
        ic = light_dark_classifier()
        rospy.init_node('LightExt2', anonymous=True)
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("Shutting down")
        cv2.destroyAllWindows()
if __name__ == '__main__':
    global font, counter
    font = cv2.FONT_HERSHEY_SIMPLEX
    light_dark_classifier.main(sys.argv)



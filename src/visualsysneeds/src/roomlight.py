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

'''
 big computational complexity: must check Light Extraction from HSV image or other approach
 '''


class RoomLight:

  def __init__(self):
    self.font = cv2.FONT_HERSHEY_SIMPLEX
    self.pub = rospy.Publisher('/opencog/roomlight', String, queue_size=10)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/usb_cam_node/image_raw",Image,self.callback)



  def Visibility(self, data, row, col):
    total=0
    for i in range(row):
        for j in range(col):
            # if not i % 3 and not j%3:
            total = total + data[i][j]
            # else:
            #     continue
    total = total/((row*col))
    if total < 50:
        return 'Dark'
    elif total < 95:
        return 'Light Dark'
    elif total < 120:
        return 'Minima'
    elif total < 165:
        return 'Normal'
    else:
        return 'Bright'


  def callback(self,data):
    try:
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        h, w = cv_image.shape[:2]
        gray2 = gray[0:h,0:w/2]
        gray3 = gray[0:h, w/2:w]

        # cv2.putText(cv_image,(self.Visibility(gray2,h, 320)),(10,240), self.font, 0.5,(255,255,255),2)
        # cv2.putText(cv_image,(self.Visibility(gray3,h, 320)),(w-100,240), self.font, 0.5,(255,255,255),2)
        # cv2.imshow('VIDEO', cv_image)

        status = (self.Visibility(gray, h, w))
        self.pub.publish(status)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit(0)
    except CvBridgeError as e:
      print(e)
def main(args):
    RoomLight()
    rospy.init_node('RoomLight', anonymous=True)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
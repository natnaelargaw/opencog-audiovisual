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
This Class contains the states and behaviours required to get the amount of light in an office/room.
 '''
class RoomLight:

  def __init__(self):
    self.pub = rospy.Publisher('/opencog/roomlight', String, queue_size=10)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/usb_cam_node/image_raw",Image,self.getLightstate)

  # Classify the frame based on the amount of pixel intensity near to white in the Grayscale equivalent
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

  # Callback function
  def getLightstate(self,data):
    try:
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        h, w = cv_image.shape[:2]

        # will be used to check for side blocks; L and R blocks
        gray2 = gray[0:h,0:w/2]
        gray3 = gray[0:h, w/2:w]

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
        print("Node RoomLight Detector Shutting Down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

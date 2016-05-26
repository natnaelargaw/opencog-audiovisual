#!/usr/bin/env python
from collections import deque
import rospy
import math
import time
from audio_common_msgs.msg import AudioData
from std_msgs.msg import String

'''
    This is a sample subscriber written to get sudden change msgs from /opencog/suddenchange topic.
 '''
class suddenChange:

  def __init__(self):
    self.loop = 0
    self.audoSub = rospy.Subscriber("/opencog/suddenchange", String, self.GetAudioClass)

  # Callback function
  def GetAudioClass(self, data):
    try:
        data = str(data)
        features = data.split("data:")[1]
        change = int(features)
        if change > 1:
            print("Sending S.change Signal to OpenCog")
        else:
            print("--> Normal Flow Indicator")
    except ArithmeticError as e:
        print(e)

if __name__ == '__main__':
    global d
    d =deque()
    try:
        rospy.init_node('suddenChange', anonymous=True)
        suddenChange()
        rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)

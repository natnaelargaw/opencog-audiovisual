#!/usr/bin/env python
from collections import deque
import rospy
import math
import time
from audio_common_msgs.msg import AudioData
from std_msgs.msg import String

'''
           This is a sample subscriber written to check the class of AudioInput. Classification is as Quite, Normal,
           Slow Music, Loud:Shout, and Very Loud: Gun Shoot.
 '''
class AudioStrength:

  def __init__(self):
    self.loop = 0
    self.audoSub = rospy.Subscriber("/opencog/AudioFeature", String, self.GetAudioClass)
 #based on my speaker performance
  def AudioEnergy(self, value):
    if value < 35:
        return 'Quite Whisper'
    elif value < 65:
        return 'Normal Conversation'
    elif value < 75:
        return 'Loud: Shouted Conversation'
    else:
        return 'Loud: Critical'

  # Callback function
  def GetAudioClass(self, data):
    try:
        data = str(data)
        features = data.split("data:")[1].split("_")
        Decibel=  float(features[0])
        Frequency =float(features[1])
        if self.loop <=2:
            d.append(Decibel)
            self.loop += 1
        else:
            d.popleft();d.append(Decibel)
            self.loop += 1
        print self.AudioEnergy(max(d))
    except ArithmeticError as e:
        print(e)

if __name__ == '__main__':
    global d
    d =deque()
    try:
        rospy.init_node('AudioClass', anonymous=True)
        AudioStrength()
        rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)

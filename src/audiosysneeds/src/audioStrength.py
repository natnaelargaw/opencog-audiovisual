#!/usr/bin/env python
from collections import deque
import rospy
import pyaudio
import math
import time
import sys
from audio_common_msgs.msg import AudioData

'''
 paragraph:
           brief code description
 '''

# Dedicated to classify the strength (Amplitude) of Real-time Audio Input
class AudioStrength:

  def __init__(self):
    self.audoSub = rospy.Subscriber("/audio",AudioData,self.GetAudioClass)
    self.audioPub = rospy.Publisher('/opencog/AudioStrength', AudioData, queue_size=10)
    self.initTime = time.time()  # time stamping


  def RMS(self, rms): # Returns the average strength of AudioData in Decibel
    SQUARE = 0
    for i in range(len(rms)):
        SQUARE = SQUARE + math.pow((rms[i]), 2)
    return  20 * math.log10(math.sqrt((SQUARE / len(rms))))


  ''' Basic classification of audio based on some threshold points --Ref-->Webmd | Subject to
  Speaker Performance '''
  def Mode(self, value): # Basic classification of audio based on some threshold points --Ref-->Webmd | Subject to Speaker Performance
    if value < 50:
        return 'Quite: Whisper'
    elif value < 75:
        return 'Normal Conversation and slow Music'
    elif value < 90:
        return 'Loud: Office Noise'
    elif value < 110:
        return 'Loud: Shouted Conversation'
    else:
        return 'Loud: Critical'


  def suddenChange(self,no, o, o2): # Purpose: Notify Significant and Sudden Decibel Change
    THRESHOLD = 10

    if o - no > THRESHOLD or o2 - no > THRESHOLD  :
        change = '1'+' ' +str(time.time()- self.initTime)
    elif o - no < -THRESHOLD or o2 - no < -THRESHOLD:
        change = '-1'+' ' +str(time.time()-self.initTime)
    else:
        change = '0'
    return change

  # Callback function
  def GetAudioClass(self,data):
    try:
        # Challenge: rospy treats unit8 [] as an array of String
        # AudioData --> int array Conversation
        tmp=str(data)
        tmp=tmp[7:tmp.__len__()-1]
        RawD = map(int, tmp.split(","))
        DECIBLE = self.RMS(RawD)
        STATE = self.Mode(DECIBLE)
        x=10
        a = x == 10 and d.append(DECIBLE) or d.popleft();d.append(DECIBLE)

        # if rospy.spin < 10: d.append(DECIBLE)
        # else: d.popleft(); d.append(DECIBLE)


        print(STATE, DECIBLE)
        self.audioPub.publish(data)
        rate.sleep()
    except ArithmeticError as e:
        print(e)

if __name__ == '__main__':
    global rate, d
    d =deque()
    try:
        rospy.init_node('AudioStrength', anonymous=True)
        AudioStrength()
        rate = rospy.Rate(5)
        rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)
        pass

#!/usr/bin/env python
from collections import deque
import rospy
import math
import time
from audio_common_msgs.msg import AudioData
from std_msgs.msg import String


'''
           This Class has two major behaviours namely: Mode and suddenChange. Mode calculates the strength
           of the latest sound in Decibels and returns its category/class as quite, loud, ... The second
           behavior returns 0 if there is sudden change that exceeds the specified threshold. Better to
           change the THRESHOLD value based on the performance of speaker on the Robot.
 '''

class AudioStrength:


  def __init__(self):
    self.loop = 0

    self.audoSub = rospy.Subscriber("/audio",AudioData,self.GetAudioClass)

    self.voiceE = rospy.Publisher('/opencog/AudioClass', String, queue_size=10)
    self.Adecibel = rospy.Publisher('/opencog/Decibel', String, queue_size=10)
    self.suddenVoice = rospy.Publisher('/opencog/suddenChange', String, queue_size=10)


    self.initTime = time.time()  # could be used for Time stamping like: at each moment, (time.time()- initTime)

  # Returns Audio Energy in Decibel
  def RMS(self, rms):
    SQUARE = 0
    for i in range(len(rms)):
        SQUARE = SQUARE + math.pow((rms[i]), 2)
    return  20 * math.log10(math.sqrt((SQUARE / len(rms))))

  # Returns Class of a given Decibel: (Ref: Webmd.com) - Must be tested and modified in the real robot mic
  def Mode(self, value):
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

  # Purpose: Notify Significant audio Energy changes
  def suddenChange(self,col):
    THRESHOLD = 10 # Test and modification of this constant is required
    return max(col) - min(col) > THRESHOLD and 1 or 0

  # Callback function
  def GetAudioClass(self, data):
    try:
        # <> rospy treats unit8 [] as an array of String; Converting to [int List]
        tmp=str(data)
        tmp=tmp[7:tmp.__len__()-1]
        RawD = map(int, tmp.split(","))

        #Get Decibel and its Class
        DECIBLE = self.RMS(RawD)
        STATE = self.Mode(DECIBLE)

        ''' Used Deque to keep the AudioEnergy Trend in the past few milli sec
            [-- <mask_size:10 ---> --> --]
        '''
        event = self.loop < 10 and d.append(DECIBLE) or \
                d.popleft();d.append(DECIBLE);
        self.loop =+ 1

        #publish: All String type msgs
        self.voiceE.publish(STATE)
        self.suddenVoice.publish(str(self.suddenChange(d)))
        self.Adecibel.publish(str(DECIBLE))
        rate.sleep()
    except ArithmeticError as e:
        print(e)

if __name__ == '__main__':
    global rate, d
    d =deque()
    try:
        rospy.init_node('AudioStrength', anonymous=True)
        AudioStrength()
        rate = rospy.Rate(1)
        rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)

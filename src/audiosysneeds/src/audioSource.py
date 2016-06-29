#!/usr/bin/env python
from collections import deque
import pyaudio
import rospy
import math
import struct
import time
import numpy as np
import re

from std_msgs.msg import String
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg


'''
   The main purpose of this Node is to publish some audio features such as Decibel and Frequency. 
   It accepts raw audio data from topic /audio published by audio_capture package.
   It publishes to two major Topics namely /opencog/AudioFeature and /opencog/change. The first one is co-
   tains Decibel and Frequency of a given chunk as a String with "Decibel_Frequency" format. The second one holds 0 -
   for No Sudden Change Events and 1 for events which have sudden change.Better to change the THRESHOLD value based on
   the performance of speaker on the Robot.
 '''

class AudioSysNeeds:

    def __init__(self):
        rospy.init_node('AudioFeature', anonymous=True)
        self.Vsource = rospy.Publisher('/opencog/AudioFeature', String, queue_size=10)
        self.Vchange = rospy.Publisher('/opencog/suddenchange', String, queue_size=10)
        rospy.Subscriber('/opencog/audio_raw_data', numpy_msg(Floats), self.audio_callback)
        self.d = deque()
        self.loop = 0
        self.RATE = 44100
        self.CHANNELS = 1
        

    # Converts Stream (which is in byte format) to List of +ve and -ve Integers
    def convData(self, V):
        count = len(V) / 2
        format = "%dh" % (count)
        shorts = struct.unpack(format, V)
        return shorts

    # The Energy of Sound per chunk is calculated
    def get_decibel(self, block):
        # get 1 val for each two char(byte)
        count = len(block) / 2
        SQUARE=0.0
        for i in block:
            SQUARE = SQUARE + math.pow(abs(i), 2)
        p = 20* math.log10(math.sqrt((SQUARE / count)))
        return p
    # Get the frequency of the current Chunk
    def getFreq(self, Maindata): # Purpose: Get the current Pitch of the file using fast fourier transform
        fftData = abs(np.fft.rfft(Maindata)) ** 2  # find the maximum
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        if which != len(fftData) - 1:
            y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            FREQUENCY = (which + x1) * self.RATE / (len(Maindata) / self.CHANNELS)
        else:
            FREQUENCY = which * self.RATE / (len(Maindata) / self.CHANNELS)
        return FREQUENCY

    # Return either 1 or 0 for Sudden Change and Similar decibels  respectively
    def suddenChanges(self, dd):
        THRESHOLD = 25 # Test and modification of this constant is required
        if max(dd)-min(dd) > THRESHOLD:
            return 10
        else:
            return 0


    def audio_callback(self, data):
        AudioRawData = np.array(data.data, dtype=np.int16)
        print len(AudioRawData)
        
        Decibel = self.get_decibel(AudioRawData)

        ''' Used Deque to keep the Audio-Energy Trend in the past few milli secs (1 sec)
            [-- <mask_size:2 ---> --> --]
        '''
        event = self.loop < 4 and self.d.append(Decibel) or \
                self.d.popleft(); self.d.append(Decibel);
        self.loop = self.loop + 1
        
        Frequency = self.getFreq(AudioRawData)
        feature= str(Decibel)+'_'+str(Frequency)
        self.Vsource.publish(feature)
        self.Vchange.publish(str(self.suddenChanges(self.d)))
        

# Entry point to Publish Three Audio Features
if __name__ == '__main__':
    
    try:
        AudioSysNeeds()
        rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)
    except rospy.ROSInitException as i:
        print (i)











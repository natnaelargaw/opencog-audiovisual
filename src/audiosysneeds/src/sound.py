#!/usr/bin/env python
import rospy

import pyaudio
import wave
import numpy as np
import math
import time


from std_msgs.msg import String #gold
initTime = time.time()  # time stamping: Done


'''
REFERENCE
- LEVEL 1: WHISPER 30
- LEVEL 2:NORMAL CONVERSATION 75
- LEVEL 3: OFFICE NOISE 90
- LEVEL 4: SHOUTED CONVERSATION 110
- LEVEL 5: CRITICAL ABOVE 120
 '''

def RMS(rms): # Purpose: return the decibel equivalent of the root mean average of Amplitude
    SQUARE = 0
    for i in range(rms.size):
        SQUARE = SQUARE + math.pow(abs(rms[i:i + 1]), 2)
    return 20* math.log10(math.sqrt((SQUARE / rms.size)))


def Mode(value): # Purpose: Classify Decibels
    print(value)
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


def suddenChange(no, o, o2): # Purpose: Notify Significant and Sudden Decibel Change
    THRESHOLD = 10
    if o - no > THRESHOLD or o2 - no > THRESHOLD  :
        change = '1'+' ' +str(time.time()-initTime)
    elif o - no < -THRESHOLD or o2 - no < -THRESHOLD:
        change = '-1'+' ' +str(time.time()-initTime)
    else:
        change='0'
    return change


def getFreq(Maindata): # Purpose: Get the current Pitch of the file using fast fourier transform
    fftData = abs(np.fft.rfft(indata)) ** 2  # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData) - 1:
        y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        FREQUENCY = (which + x1) * RATE / chunk
    else:
        FREQUENCY = which * RATE / chunk
    return FREQUENCY

def entrypoint():
    old = 0
    older = 0
    chunk = 8192  # open up a wave - sample points are 8192
    # Entry Point
    wf = wave.open('src/audiosysneeds/src/singing-female.wav', 'rb')
    swidth = wf.getsampwidth()
    RATE = wf.getframerate()
    # use a Blackman window
    window = np.blackman(chunk)  # open stream
    p = pyaudio.PyAudio()
    stream = p.open(format=
                    p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=RATE,
                    output=True)
    data = wf.readframes(chunk)

    pub = rospy.Publisher('AudioMode', String, queue_size=10)
    pub1 = rospy.Publisher('AudioDecibel', String, queue_size=10)
    pub2 = rospy.Publisher('AudiosuddenChange', String, queue_size=10)

    rospy.init_node('sound', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while len(data) == chunk * swidth and not rospy.is_shutdown():
        # o/p
        stream.write(data)
        # unpacked data * the hamming window
        indata = np.array(wave.struct.unpack("%dh" % (len(data) / swidth), data)) * window

        DECIBLE = RMS(indata)
        STATE = Mode(DECIBLE)

        data = wf.readframes(chunk)
        older = old
        old=DECIBLE

        audiMode = str(STATE)
        strength = str(DECIBLE)
        changes = str(suddenChange(DECIBLE, old, older))
        rospy.loginfo(STATE)
        rospy.loginfo(DECIBLE)
        rospy.loginfo(changes)
        pub.publish(audiMode)
        pub1.publish(strength)
        pub2.publish(changes)

        rate.sleep()
if __name__ == '__main__':

    try:
        entrypoint()
    except rospy.ROSInterruptException:
        pass

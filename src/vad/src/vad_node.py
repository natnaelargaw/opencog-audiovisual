#!/usr/bin/env python
import wave
import rospy
from ltsd_vad import *
import numpy as np
import matplotlib.pyplot as plt
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
import pyaudio

big_data = []
WINSIZE = 10000
SAMPLE_RATE = 44100
counter = 0

vad_pub = rospy.Publisher('/voice_activity', numpy_msg(Floats), queue_size=10)

#audio = pyaudio.PyAudio()
#stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True)

def fence(va, size):
	start = 0
	end = 0
	for i in range(len(va)):
		start = i if (va[i] > 11) and (start == 0) else start
		end = (i-1) if (va[i] < 11 or i == (len(va)-1)) and start != 0 else 0
	
	start = float(size*start)/len(va)
	end = float(size*end)/len(va)
	return int(start), int(end)



def vad_callback(data):
	global big_data; global WINSIZE; global vad_pub; global stream; global SAMPLE_RATE
	global counter
	signal = np.array(data.data, dtype=np.int16)
	#stream.write(np.asarray(signal))
	print "recieved = " + str(len(signal)) + " frames = " + str(float(len(signal))/SAMPLE_RATE) + " seconds"
	#signal = np.asarray(big_data)
	
	
	fo = wave.open('out_data_'+str(counter), 'wb')
	fo.setnchannels(1)
	fo.setframerate(SAMPLE_RATE)
	fo.setsampwidth(2)
	fo.writeframes(signal)
	fo.close()
	counter += 1
	
	window = sp.hanning(WINSIZE)
	ltsd = LTSD(WINSIZE,window,5)
	res =  ltsd.compute(signal)
	start, end = fence(res, len(signal))
	final = np.array(signal[start:end],dtype=np.float32)
	if start != end:
		#there is speech activity in the sample
		print "FOUND ACTIVITY - " + str(max(final))
		vad_pub.publish(final)
		

if __name__=="__main__":
    try:
    	rospy.init_node('VAD', anonymous=True)
    	rospy.Subscriber('/audio_raw_data', numpy_msg(Floats), vad_callback)
    	rospy.spin()
    except ROSInitException as i:
    	print str(i)
    except ROSInterruptException as e:
    	print str(e)
    

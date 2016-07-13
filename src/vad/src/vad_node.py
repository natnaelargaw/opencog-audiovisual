#!/usr/bin/env python

'''
	left out the filter because the vad isn't very good.
	when a non-silence audio is catagorized as silence or just white noise 
	and is used for filtering (subtraction), the result is just high quality distortion.
	Without the filter, if there's a single dominant speaker, it works fine.
'''

import wave
import rospy
from ltsd_vad import *
import numpy as np
import matplotlib.pyplot as plt
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
import pyaudio
import scipy as sp
from numpy import matlib
from scipy import linalg

big_data = []
WINSIZE = 3500
SAMPLE_RATE = 16000
counter = 0
BITWIDTH = 16
background_noise = []
FILTER = False
vad_pub = rospy.Publisher('/opencog/voice_activity', numpy_msg(Floats), queue_size=10)


#audio = pyaudio.PyAudio()
#stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True)

def cocktail(data1, data2):
	global BITWIDTH
	dt1 = data1 / float(1<<(BITWIDTH-1))
	dt2 = data2 / float(1<<(BITWIDTH-1))
	xx = [dt1, dt2]
	p = xx - np.transpose(matlib.repmat(np.mean(xx, 1), np.shape(xx)[1], 1))
	yy = np.dot(linalg.sqrtm(np.linalg.inv(np.cov(xx))), p)
	rr = matlib.repmat(np.sum(yy*yy, 0), np.shape(yy)[0], 1)
	w, s, v = np.linalg.svd(np.dot(rr*yy, np.transpose(yy)))
	f = np.transpose(np.dot(np.transpose(xx), w)) #w is the unmixing matrix
	f[0] *= float(1<<(BITWIDTH-1))
	f[1] *= float(1<<(BITWIDTH-1))
	return f


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
	global counter; global background_noise; global FILTER
	signal = np.array(data.data, dtype=np.int16)
	#stream.write(np.asarray(signal))
	print "recieved = " + str(len(signal)) + " frames = " + str(float(len(signal))/SAMPLE_RATE) + " seconds"
	#signal = np.asarray(big_data)
	
	window = sp.hanning(WINSIZE)
	ltsd = LTSD(WINSIZE,window,5)
	res =  ltsd.compute(signal)
	start, end = fence(res, len(signal))
	final = np.array(signal[start:end],dtype=np.float32)
	print 'start = ' + str(start)
	print 'end   = ' + str(end)
	if end - start > SAMPLE_RATE/2:
		#there is speech activity in the sample
		#print signal
		print "FOUND ACTIVITY - " + str(max(final))
		
		if FILTER and len(background_noise) > 0: #if activity is grater than half a sec:
			#take the last bg_noise in the list for better filtering
			f = cocktail(signal, background_noise[len(background_noise)-1])
			vad_pub.publish(np.array(f[0], dtype=np.float32))
		else:
			vad_pub.publish(np.array(signal, dtype=np.float32))
	else:
		if FILTER:
			background_noise.append(signal)
			if len(background_noise) > 5:
				background_noise = []
				background_noise.append(signal)

if __name__=="__main__":
    try:
    	rospy.init_node('VAD', anonymous=True)
    	rospy.Subscriber('/opencog/audio_raw_data', numpy_msg(Floats), vad_callback)
    	rospy.spin()
    except ROSInitException as i:
    	print str(i)
    except ROSInterruptException as e:
    	print str(e)
    

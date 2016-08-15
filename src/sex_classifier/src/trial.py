#!/usr/bin/env python
import rospy
import numpy as np
import pyaudio
from audio_common_msgs.msg import AudioData
import re
import struct
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
from std_msgs.msg import Int16MultiArray
import wave
import matplotlib.pyplot as plt

'''
	This is only an experimental code. 
'''



audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, 
					rate=16000, output=True)
f = wave.open('trial_output.wav', 'wb')
f.setnchannels(1)
f.setsampwidth(2)
f.setframerate(16000)
data_write = []

def convData(V):
    count = len(V) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, V)
    return shorts


def callback(data):
	global stream
	global data_write
	global f
	#d = re.findall(r'\d+', data.__str__())
	#d = [int(i) for i in d]
	print "printing data --------------------------"
	print "data"
	print "printing the type +++++++++++++++++++++"
	print type(data)
	print type(data.data)

	d = np.array(data.data, dtype=np.int16)
	#d = []
	#d = np.asarray(d)
	#d = data.deserialize_numpy(data.data, d)
	#d = re.findall(r'\d+', data.__str__())
	#d = [int(i) for i in d]
	#d = np.array(data.data, dtype = tuple)
	#d = np.array(data,dtype = AudioData)
	print '-----------------------------------------'
	
	print np.shape(d)
	print d
	stream.write(np.asarray(d))
	
	
	'''
	if(len(data_write) > 88200):
		plt.plot(data_write)
		plt.show()
		#data_write = data_write[:22050]
		#stream.write(np.asarray(data_write))
		data_write = []
	else:
		data_write += list(d)
	'''


rospy.init_node('trial_node', anonymous=True)
#rospy.Subscriber('/audio_pub', Int16MultiArray, callback)
#rospy.Subscriber('/audio', AudioData, callback)
rospy.Subscriber('/opencog/audio_raw_data',numpy_msg(Floats), callback)

try:
	rospy.spin()
except ROSInitException as e:
	print(e) 

audio.close(stream)
f.writeframes(data_write.__str__())
f.close()

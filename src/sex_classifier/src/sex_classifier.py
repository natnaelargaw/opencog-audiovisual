#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import numpy as np
import sys
import os
from sklearn.svm import LinearSVC
from utilities import *
import struct
import pickle
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
import pyaudio

class sex_classifier:
	def __init__(self):
		self.PLAYBACK = False

		rospy.init_node('Sex_Classifier', anonymous=True)
		rospy.Subscriber('/opencog/voice_activity', numpy_msg(Floats), self.callback) #sub to pcm data from VAD
		self.sex_publisher = rospy.Publisher('/opencog/speaker_sex', String, queue_size=1)
		file_name = os.path.join(
			os.path.dirname(os.path.realpath(__file__)), 'model/pickle_dump.pkl')
		self.svm = pickle.load(open(file_name, 'r'))
		if self.PLAYBACK:
			self.audio = pyaudio.PyAudio()
			self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, 
						rate=16000, output=True, frames_per_buffer=1)
		self.sample_rate = 16000
		
		self.MALE = 1

	def convData(self, V):
	    count = len(V) / 2
	    format = "%dh" % (count)
	    shorts = struct.unpack(format, V)
	    return shorts

	#to do feature extraction on data without silence
	def callback(self, data):
		data  = np.array(data.data,dtype = np.int16)
		if self.PLAYBACK:
			self.stream.write(np.asarray(data))
		#data = self.convData(data.data)
		data_no_silence = no_silence(data, self.sample_rate) #remove all silence part from audio
		features = feature_extraction(data_no_silence, self.sample_rate, 0.05*self.sample_rate, 0.025*self.sample_rate)
		print "feature shape = " + str(np.shape(features))
		features = features.transpose()
		res = self.svm.predict(features) #transpose cuz sklearn accepts [samples][features] format
		res = res.tolist()
		male_confidence = (float(res.count(self.MALE))/len(res)) * 100
		sex_str = 'Male' if male_confidence > 50 else 'Female'
		sex_str += ' - confidence = ' + str(male_confidence) if male_confidence > 50 else str(100 - male_confidence)
		self.sex_publisher.publish(sex_str)
		#print 'male' if male_confidence > 50 else 'female'
		#print 'confidence = ' + str(male_confidence) if male_confidence > 50 else str(100 - male_confidence)


if __name__ == '__main__':
	try:
		sex_classifier()
		rospy.spin()
	except rospy.ROSInterruptException as e:
		print str(e)



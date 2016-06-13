#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import numpy as np
import sys
import os
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from utilities import *
import struct

class sex_classifier:

	sample_rate = 44100

	def __init__(self):
		rospy.init_node('Sex_Classifier', anonymous=True)
		rospy.Subscriber('/opencog/audio_raw_data', String, self.callback) #sub to pcm data
		rospy.Subscriber('/opencog/AudioFeature', String, self.source_callback)
		self.svm = LinearSVC()
		self.svm = joblib.load(os.path.join(
			os.path.dirname(os.path.realpath(__file__)), 'model/good_model.pkl'))

	def convData(self, V):
	    count = len(V) / 2
	    format = "%dh" % (count)
	    shorts = struct.unpack(format, V)
	    return shorts

	def source_callback(self, data):
		self.sample_rate = int(str(data).split('_')[1])
		

	#to do feature extraction on data without silence
	def callback(self, data):
		data = self.convData(data.data)
		data_no_silence = no_silence(data, self.sample_rate) #remove all silence part from audio
		features = feature_extraction(data_no_silence, self.sample_rate, 0.05*self.sample_rate, 0.025*self.sample_rate)
		res = self.svm.predict(features.transpose()).tolist() #transpose cuz sklearn accepts [samples][features] format
		male_confidence = (float(res.count(0))/len(res)) * 100
		print 'male' if male_confidence > 50 else 'female'
		print 'confidence = ' + str(male_confidence) if male_confidence > 50 else str(100 - male_confidence)


if __name__ == '__main__':
	try:
		sex_classifier()
		rospy.spin()
	except rospy.ROSInterruptException as e:
		print str(e)

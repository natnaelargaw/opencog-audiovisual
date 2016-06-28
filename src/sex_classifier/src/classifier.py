#!/usr/bin/env python
import numpy as np 
from scipy.io import wavfile
from utilities import *
import sys
import pickle
import matplotlib.pyplot as plt


file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'model/pickle_dump.pkl')
svm = pickle.load(open(file_name, 'r'))

smp, data = wavfile.read(sys.argv[1])
print "data length = " + str(len(data))
data_no_silence = no_silence(data, smp, plot=True) #remove all silence part from audio
print "length of no silence = " + str(len(data_no_silence))
features = feature_extraction(data_no_silence, smp, 0.05*smp, 0.025*smp)
print "feature shape = " + str(np.shape(features))
features = features.transpose()
res = svm.predict(features) #transpose cuz sklearn accepts [samples][features] format
res = res.tolist()
male_confidence = (float(res.count(1))/len(res)) * 100
print 'male' if male_confidence > 50 else 'female'
print 'confidence = ' + str(male_confidence) if male_confidence > 50 else str(100 - male_confidence)

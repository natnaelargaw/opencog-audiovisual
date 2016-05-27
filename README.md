##Simple Auditory and  Visual System Needs for OpenCog
------------

##Introduction
------------
  This package is built with the intention of addressing the following user requirements.
###Audio
------------
1. Sudden Change Detection
</br>
  To make the robot detect significant changes -audio. e.g some one yelling at the robot  all of the sudden.
2. Sound Classification
</br>
  Classifying each chunk of sound as quite, normal conversation, shouted conversation, very loud sound like gunshot.
3. Sex Perception
</br>
  Detecting speaker's Gender based on thier audio utterance.
4. Speakers Counting
</br>
  Detecting the number of speakers/talking folks from real-time gathered audio data.
5. Speakers Speed
</br>
  Answers how fast is the person Talking
</br>

###Visual
------------
1. Visibility Checkup
</br>
  Check the amount of light in a given room. e.g In the case of dark room, informing the system about the situation and interacting w/ the user in based on the context (like i can't see you, some one is blocking me, bla bla).
2. Room Silence
</br>
  Detect how placid/chaotic the room is.
3. Room Occupation
</br>
  To answer questions such as any available subject in the room lately? How many?

##Requirements and Setup
------------
 - Middle ware     - ROS/indigo
 - Dev. Language   - Python v2.7/rospy
 - Audio Package   - PyAudiov0.2.9
 - Vison Package   - Opencv v2.4.13
</br> 
Install them using the following shell script
</br> 
  `cd && bash git_folder/env_setup.sh`
</br>

##Building
------------ 
</br>
 `cd your_work_space &&  source devel/setup.bash`

##Usage
------------
  TBW

###Topics 
1. /opencog/decibels
  - message type:
  - Value:
2. /opencog/suddenchange
  - message type: 
  - Value:
3. /opencog/roomlight
  - message type:
  - Value:
4. /opencog/roomoccupation
  - message type:
  - Value:
5. /opencog/roomsilence
  - message type:
  - Value:
6. /opencog/sex
  - message type:
  - Value:
7. /opencog/speakersNo
  - message type:
  - Value:

##Troubleshooting
------------
  TBW

##FAQ
------------
  TBW
</br>

##Reference

##Employed Techniques and Algorithms
------------
- [Root Mean Square (RMS)](http://www.gaussianwaves.com/2015/07/significance-of-rms-root-mean-square-value/)
- [Frequency Detection] (https://gist.github.com/endolith/255291) 
- [Image Smoothing] (https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=13&cad=rja&uact=8&ved=0ahUKEwjintiowvnMAhVLPhQKHRJbBtAQFghaMAw&url=https%3A%2F%2Fdocs.gimp.org%2Fen%2Fplug-in-gauss.html&usg=AFQjCNFAfO3cTIjyIMdW8htt6qZsa1HXvg)
- [Background Subtraction](http://docs.opencv.org/2.4/doc/tutorials/imgproc/threshold/threshold.html)
- [Image Morphology] (https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwjv3bTawvnMAhWDxRQKHQM2B18QFgggMAA&url=http%3A%2F%2Fwww.mathworks.com%2Fhelp%2Fimages%2Fmorphological-dilation-and-erosion.html&usg=AFQjCNG6mcuUFffnwnnb4wZrYI-cKarYAg)
- [Moving Collections] (https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=0ahUKEwjm6uvpwvnMAhXEWxQKHScbBwsQFggnMAE&url=https%3A%2F%2Fdocs.python.org%2F3%2Flibrary%2Fcollections.html&usg=AFQjCNG2mjapHqnnZgJmeiKpa724xaH-wg)

##Limitations and Feature works
------------
TBW

###Audio System Needs
------------
 The audio related features are tested based on two audio sources. Hence, some code rearrangement shall be done to make it work on the real robot.

###Visual System Needs
------------
 The room occupation and silence nodes are based on the size and number of contours on filtered and background subtracted images. The nearer the ROI the higher its impact is. (e.g. man waving his hand near to the front camera). Hence, incorporating depth data of ROI's should be the next task here.








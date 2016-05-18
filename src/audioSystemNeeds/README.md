#opencog-audio -Under Development	
## Installation
* cd opencog-audiovisual
* bash setup.sh

# Running the code
* ctrl +alt + t
* roscore
* ctrl + shift + t
* cd opencog-audiovisual/src/audioSystemNeeds/src/
* chmod +x sound.py
* cd ../../..
* source devel/setup.bash
* catkin_make
* rosrun audioSystemNeeds sound.py

# Topics
The decibel, the Intensity Trend and The boolean resut for the sudden change checker is published to
/AudioDecibel, /AudioMode, and /AudiosuddenChange respectively.





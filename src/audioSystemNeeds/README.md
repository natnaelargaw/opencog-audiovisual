## Installation
* cd audioSystemNeeds
* bash setup.sh

# Running the code
* ctrl +alt + t
* roscore
* ctrl + shift + t
* cd audioSystemNeeds/src/simpleauditory/src
* chmod +x sound.py
* cd ../../.. && catkin_make
* source devel/setup.bash
* rosrun simpleauditory sound.py

# Topics
The decibel, the Intensity Trend and The boolean resut for the sudden change checker is published to
/AudioDecibel, /AudioMode, and /AudiosuddenChange respectively.





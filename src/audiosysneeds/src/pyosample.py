#!/usr/bin/env python
from pyo import *
import time
import rospy
from std_msgs.msg import String #gold
def entrypoint():
     pub = rospy.Publisher('checkpyo', String, queue_size=10)
     rospy.init_node('pyosample', anonymous=True)
     rate = rospy.Rate(10) # 10hz
     while not rospy.is_shutdown():
        rospy.loginfo('Hello')
        pub.publish('Hello')
        time.sleep(10)
     s.stop()


if __name__ == '__main__':
    s = Server(duplex=0)
    #s.setInOutDevice(2)
    s.boot()
    s.start()
    a = Sine(mul=1).out()
    try:
        entrypoint()
    except rospy.ROSInterruptException:
        pass










#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState


global pub_pan, pub_cmd



def jointStateCallback(jointStateData):

    global pub_pan

    pan_joint=JointState()
    position=[jointStateData.position[12]]
    pan_joint.position=position
    pub_pan.publish(pan_joint)


def panCallback(panData):

    global pub_cmd

    pan_cmd=Float64()
    pan_cmd.data=panData.data
    pub_cmd.publish(pan_cmd)



def global_planner():

    global pub_pan, pub_cmd

    #ROS init
    rospy.init_node('virtual_pan', anonymous=True)

    #gazebo->robot
    pub_pan = rospy.Publisher('/pan/joint_states', JointState, queue_size=1)
    rospy.Subscriber("/joint_states", JointState, jointStateCallback)

    #robot->gazebo
    pub_cmd = rospy.Publisher('/pan_controller/command', Float64, queue_size=1)
    rospy.Subscriber("/pan/pan_position_controller/command", Float64, panCallback)


    #main loop
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        #check
        rate.sleep()

if __name__ == '__main__':
    try:
        global_planner()
    except rospy.ROSInterruptException:
        pass


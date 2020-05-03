#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
from dji_sdk.msg import Gimbal


global pub_r, pub_p, pub_y


def gimbalCallback(gimbalData):

    global pub_r, pub_p, pub_y

    roll=Float64()
    pitch=Float64()
    yaw=Float64()

    roll.data=gimbalData.pitch
    pitch.data=gimbalData.roll
    yaw.data=gimbalData.yaw

    pub_r.publish(roll)
    pub_p.publish(pitch)
    pub_y.publish(yaw)


def global_planner():

    global pub_r, pub_p, pub_y

    #ROS init
    rospy.init_node('virtual_gimbal', anonymous=True)

    pub_r = rospy.Publisher('/roll_controller/command', Float64, queue_size=1)
    pub_p = rospy.Publisher('/pitch_controller/command', Float64, queue_size=1)
    pub_y = rospy.Publisher('/yaw_controller/command', Float64, queue_size=1)
    rospy.Subscriber("/dji_sdk/gimbal_angle_cmd", Gimbal, gimbalCallback)

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


#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
from dji_sdk.msg import Gimbal
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Vector3Stamped


global pub_r, pub_p, pub_y, pub_angle, roll, pitch, yaw



def gimbalCallback(gimbalData):

    global pub_r, pub_p, pub_y, roll, pitch, yaw

    if gimbalData.mode == 0:
        roll.data=roll.data+gimbalData.roll
        pitch.data=pitch.data+gimbalData.pitch
        yaw.data=yaw.data+gimbalData.yaw

    else :
        roll.data=gimbalData.roll
        pitch.data=gimbalData.pitch
        yaw.data=gimbalData.yaw

    pub_r.publish(roll)
    pub_p.publish(pitch)
    pub_y.publish(yaw)




def gimbalAngleCallback(gimbalJointData):

    global pub_angle

    gimbal_angle=Vector3Stamped()

    gimbal_angle.vector.x=gimbalJointData.position[8]
    gimbal_angle.vector.y=gimbalJointData.position[9]
    gimbal_angle.vector.z=gimbalJointData.position[10]

    pub_angle.publish(gimbal_angle)


def global_planner():

    global pub_r, pub_p, pub_y, pub_angle, roll, pitch, yaw

    #ROS init
    rospy.init_node('virtual_gimbal', anonymous=True)

    pub_r = rospy.Publisher('/roll_controller/command', Float64, queue_size=1)
    pub_p = rospy.Publisher('/pitch_controller/command', Float64, queue_size=1)
    pub_y = rospy.Publisher('/yaw_controller/command', Float64, queue_size=1)
    rospy.Subscriber("/dji_sdk/gimbal_angle_cmd", Gimbal, gimbalCallback)

    pub_angle = rospy.Publisher('/dji_sdk/gimbal_angle', Vector3Stamped, queue_size=1)
    rospy.Subscriber("/joint_states", JointState, gimbalAngleCallback)

    roll=Float64()
    pitch=Float64()
    yaw=Float64()

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


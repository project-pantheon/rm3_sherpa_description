#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <tf/transform_listener.h>
#include <gazebo_msgs/ModelState.h>
#include <geometry_msgs/Point.h>
#include <geometry_msgs/Quaternion.h>
#include <nav_msgs/Odometry.h>


nav_msgs::Odometry m_odom_msg;

void odomChanged(const nav_msgs::Odometry::ConstPtr& msg)
{
    m_odom_msg = *msg;

}

int main(int argc, char** argv){

    //Calling the ros init function
    ros::init(argc, argv, "arrow");

    //Ros node handler
    ros::NodeHandle n;

    //Ros rate
    ros::Rate r(100);

    //broadcaster sends data
    tf::TransformBroadcaster broadcaster;
    
    //listener asks data    
    tf::TransformListener listener;

    geometry_msgs::Point position;
    position.x=0;
    position.y=0;
    position.z=0;

    //90 degress on pitch to turn the camera down
    geometry_msgs::Quaternion orientation;
    orientation.x=0;
    orientation.y=0;
    orientation.z=0;
    orientation.w=1;
    

    ros::Publisher arrow_pub = n.advertise<gazebo_msgs::ModelState>("/gazebo/set_model_state", 1);

    gazebo_msgs::ModelState arrow_state;


    ros::Subscriber sub_odom = n.subscribe("/ekf_localization_slam_node/slam_odom_magnetic", 1, odomChanged);
    

    while(n.ok()){
        

        tf::StampedTransform transform;
        try{
            listener.lookupTransform("map", "sherpa/base_link",  
                                   ros::Time(0), transform);
            ROS_INFO("ok");
        }
        catch (tf::TransformException ex){

        }

        position.x = transform.getOrigin().x();
        position.y = transform.getOrigin().y();

        arrow_state.model_name="camera_gui"; //name of the MODEL on gazebo 
        arrow_state.pose.position=position;
        arrow_state.pose.orientation=orientation;
        arrow_state.reference_frame="map"; //reference FRAME

        arrow_pub.publish(arrow_state);

        // send position
        broadcaster.sendTransform(
        tf::StampedTransform(
            tf::Transform(tf::Quaternion(orientation.x, orientation.y, orientation.z, orientation.w), tf::Vector3(position.x, position.y, position.z)),
        ros::Time::now(),"/map", "/arrow_baselink"));

        ros::spinOnce();
        r.sleep();
    }
}

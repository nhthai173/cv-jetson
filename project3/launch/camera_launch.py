from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='camera_pkg',
            namespace='camera_pkg',
            executable='listener',
            output='screen',
            name='sim'
        ),
        Node(
            package='camera_pkg',
            namespace='camera_pkg',
            executable='talker',
            output='screen',
            name='sim'
        ),
    ])
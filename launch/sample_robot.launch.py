import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
  pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
  worlds = os.path.join(get_package_share_directory('sample_diff_drive_control'), 'world', 'willow_garage.world')

  urdf = os.path.join(get_package_share_directory('sample_diff_drive_control'), 'urdf', 'sample_robot.urdf')

  use_sim_time = LaunchConfiguration('use_sim_time', default='true')

  return LaunchDescription([

    DeclareLaunchArgument(
      'world',
      default_value=[worlds, ''],
      description='SDF world file'
    ),

    Node(
      package='robot_state_publisher',
      executable='robot_state_publisher',
      name='robot_state_publisher',
      arguments=[urdf],
    ),

    Node(
      package='joint_state_publisher',
      executable='joint_state_publisher',
      name='joint_state_publisher',
      arguments=[urdf],
    ),

    IncludeLaunchDescription(
      PythonLaunchDescriptionSource(
        os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py'),
      )
    ),

    Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        name="urdf_spawner",
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=[
          "-topic", "/robot_description",
          "-entity", "sample_robot",
          "-x", "-9",
          "-y", "-17",
          "-z", "0.88",
          "-Y", "1.57",
        ]
    ),
  ])

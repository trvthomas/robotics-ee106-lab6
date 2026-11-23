import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (AppendEnvironmentVariable, DeclareLaunchArgument,
                            IncludeLaunchDescription, GroupAction)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution



ARGUMENTS = [
    DeclareLaunchArgument('namespace', default_value='', description='Robot namespace'),
    DeclareLaunchArgument('rviz', default_value='false', choices=['true', 'false'], description='Start rviz.'),
    DeclareLaunchArgument('world', default_value='straight_line', description='Simulation World: name of a .sdf file in ee106f26/worlds (without the extension), or the name of a TurtleBot4 world, i.e. empty'),
    DeclareLaunchArgument('model', default_value='lite', choices=['standard', 'lite'], description='Turtlebot4 Model'),
]

for pose_element in ['x', 'y', 'z', 'yaw']:
    ARGUMENTS.append(DeclareLaunchArgument(pose_element, default_value='0.0', description=f'{pose_element} component of the robot pose.'))


def generate_launch_description():
    # Directories
    pkg_turtlebot4_gz_bringup = get_package_share_directory(
        'turtlebot4_gz_bringup')
    pkg_ee106f26 = get_package_share_directory(
        'ee106f26')

    # Paths
    gazebo_launch = PathJoinSubstitution(
        [pkg_turtlebot4_gz_bringup, 'launch', 'sim.launch.py'])
    robot_spawn_launch = PathJoinSubstitution(
        [pkg_ee106f26, 'launch', 'turtlebot_spawn.launch.py'])

    # The TurtleBot4 sim.launch.py looks for the world as '<world>.sdf' in the
    # Gazebo resource path. Our worlds folder is added to the path, so that
    # ee106f26/worlds/<world>.sdf is found directly.
    # set_world_path = AppendEnvironmentVariable(
    #     'GZ_SIM_RESOURCE_PATH', os.path.join(pkg_ee106f26, 'worlds'))

    gazebo = GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([gazebo_launch]),
            launch_arguments=[
                ('world', PathJoinSubstitution(
                    [pkg_ee106f26, 'worlds', LaunchConfiguration('world')]))
            ]
        )
    ])


    # Includes the launch description of the robot
    # This loads the models of the components, and any other packages
    # required for spawning the robot
    robot_spawn = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([robot_spawn_launch]),
        launch_arguments=[
            ('model', LaunchConfiguration('model')),
            ('namespace', LaunchConfiguration('namespace')),
            ('rviz', LaunchConfiguration('rviz')),
            ('x', LaunchConfiguration('x')),
            ('y', LaunchConfiguration('y')),
            ('z', LaunchConfiguration('z')),
            ('yaw', LaunchConfiguration('yaw'))]
    )

    # Create launch description and add actions
    ld = LaunchDescription(ARGUMENTS)
    # ld.add_action(set_world_path)
    ld.add_action(gazebo)
    ld.add_action(robot_spawn)
    return ld
from launch import LaunchDescription
from launch_ros.actions import Node, SetParameter
from launch.substitutions import  PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution
)


def generate_launch_description():
    use_sim = LaunchConfiguration("use_sim")
    declare_use_sim_arg = DeclareLaunchArgument(
        "use_sim",
        default_value="False",
        description="Whether simulation is used",
    )

    simulation_engine = LaunchConfiguration("simulation_engine")
    declare_simulation_engine_arg = DeclareLaunchArgument(
        "simulation_engine",
        default_value="webots",
        description="Which simulation engine to be used",
        choices=["ignition-gazebo", "gazebo-classic", "webots"]
    )


    rosbot_controller = get_package_share_directory("rosbot_controller")
    rosbot_bringup = get_package_share_directory("rosbot_bringup")

    rosbot_controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    rosbot_controller,
                    "launch",
                    "controller.launch.py",
                ]
            )
        ),
        launch_arguments={
            "use_sim": use_sim,
            "simulation_engine": simulation_engine,
        }.items(),
    )

    ekf_config = PathJoinSubstitution([rosbot_bringup, "config", "ekf.yaml"])

    robot_localization_node = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node",
        output="screen",
        parameters=[ekf_config],
    )

    actions = [
        declare_use_sim_arg,
        declare_simulation_engine_arg,
        SetParameter(name="use_sim_time", value=use_sim),
        rosbot_controller_launch,
        robot_localization_node
    ]

    return LaunchDescription(actions)

#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand, VehicleLocalPosition, VehicleStatus, VehicleGlobalPosition
from rclpy.executors import MultiThreadedExecutor
import threading

x, y, z = 0., 10., 0.
dx, dy, dz = 0., 10., 0.
stop_flag = False

class OffboardControl(Node):
    """Node for controlling a vehicle in offboard mode."""

    def __init__(self, id) -> None:
        global x, y, z
        super().__init__('offboard_control_takeoff_and_land')
        print("id : ",id," x: ",x," y: ",y," z: ",z)

        # Configure QoS profile for publishing and subscribing
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        self.setpointx = 0.
        self.setpointy = 0.
        self.setpointz = 0.
        self.id = id
        # Create publishers
        self.offboard_control_mode_publisher = self.create_publisher(
            OffboardControlMode, '/px4_'+str(id)+'/fmu/in/offboard_control_mode', qos_profile)
        self.trajectory_setpoint_publisher = self.create_publisher(
            TrajectorySetpoint, '/px4_'+str(id)+'/fmu/in/trajectory_setpoint', qos_profile)
        self.vehicle_command_publisher = self.create_publisher(
            VehicleCommand, '/px4_'+str(id)+'/fmu/in/vehicle_command', qos_profile)

        # Create subscribers
        self.vehicle_local_position_subscriber = self.create_subscription(
            VehicleLocalPosition, '/px4_'+str(id)+'/fmu/out/vehicle_local_position', self.vehicle_local_position_callback, qos_profile)
        self.vehicle_status_subscriber = self.create_subscription(
            VehicleStatus, '/px4_'+str(id)+'/fmu/out/vehicle_status', self.vehicle_status_callback, qos_profile)
        self.vehicle_global_position_subscriber = self.create_subscription(
            VehicleGlobalPosition, '/px4_'+str(id)+'/fmu/out/vehicle_global_position', self.vehicle_global_position_callback, qos_profile)

        # Initialize variables
        self.offboard_setpoint_counter = 0
        self.vehicle_local_position = VehicleLocalPosition()
        self.vehicle_status = VehicleStatus()
        self.takeoff_height = -5.
        self.vehicle_global_position = VehicleGlobalPosition()

        # Create a timer to publish control commands
        self.timer = self.create_timer(0.1, self.timer_callback)

    def vehicle_local_position_callback(self, vehicle_local_position):
        """Callback function for vehicle_local_position topic subscriber."""
        self.vehicle_local_position = vehicle_local_position

    def vehicle_status_callback(self, vehicle_status):
        """Callback function for vehicle_status topic subscriber."""
        self.vehicle_status = vehicle_status

    def vehicle_global_position_callback(self, vehicle_global_position):
        self.vehicle_global_position = vehicle_global_position

    def arm(self):
        """Send an arm command to the vehicle."""
        self.publish_vehicle_command(
            VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, param1=1.0)
        self.get_logger().info('Arm command sent')

    def disarm(self):
        """Send a disarm command to the vehicle."""
        self.publish_vehicle_command(
            VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, param1=0.0)
        self.get_logger().info('Disarm command sent')

    def engage_offboard_mode(self):
        """Switch to offboard mode."""
        self.publish_vehicle_command(
            VehicleCommand.VEHICLE_CMD_DO_SET_MODE, param1=1.0, param2=6.0)
        self.get_logger().info("Switching to offboard mode")

    def land(self):
        """Switch to land mode."""
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_LAND)
        self.get_logger().info("Switching to land mode")

    def publish_offboard_control_heartbeat_signal(self):
        """Publish the offboard control mode."""
        msg = OffboardControlMode()
        msg.position = True
        msg.velocity = False
        msg.acceleration = False
        msg.attitude = False
        msg.body_rate = False
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.offboard_control_mode_publisher.publish(msg)

    def publish_position_setpoint(self, x: float, y: float, z: float):
        """Publish the trajectory setpoint."""
        msg = TrajectorySetpoint()
        msg.position = [x, y, z]
        msg.yaw = 1.57079  # (90 degree)
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.trajectory_setpoint_publisher.publish(msg)
        self.get_logger().info(f"Publishing position setpoints {[x, y, z]}")

    def publish_vehicle_command(self, command, **params) -> None:
        """Publish a vehicle command."""
        msg = VehicleCommand()
        msg.command = command
        msg.param1 = params.get("param1", 0.0)
        msg.param2 = params.get("param2", 0.0)
        msg.param3 = params.get("param3", 0.0)
        msg.param4 = params.get("param4", 0.0)
        msg.param5 = params.get("param5", 0.0)
        msg.param6 = params.get("param6", 0.0)
        msg.param7 = params.get("param7", 0.0)
        msg.target_system = self.id + 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.vehicle_command_publisher.publish(msg)

    def moveto(self, x, y, z):
        self.setpointx, self.setpointy, self.setpointz = float(x), float(y), float(z)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def local_pos(self):
        return [self.vehicle_local_position.x, self.vehicle_local_position.y, self.vehicle_local_position.z]

    def global_pos(self):
        return [self.vehicle_global_position.lat, self.vehicle_global_position.alt, self.vehicle_global_position.lon]


    def timer_callback(self) -> None:
        """Callback function for the timer."""
        self.publish_offboard_control_heartbeat_signal()

        if self.offboard_setpoint_counter == 10:
            self.engage_offboard_mode()
            self.arm()

        if self.vehicle_status.nav_state == VehicleStatus.NAVIGATION_STATE_OFFBOARD:
            self.publish_position_setpoint(self.setpointx, self.setpointz, -self.setpointy)

        if self.offboard_setpoint_counter < 11:
            self.offboard_setpoint_counter += 1

#Create an executor and an array of "number" nodes ,starts the executor and return the array of nodes
def drone_init(number):
    global executor, thread
    executor = MultiThreadedExecutor()

    nodes = []
    for i in range(1, number+1):
        node = OffboardControl(i)
        executor.add_node(node)
        nodes.append(node)

    # Create a thread to spin the executor
    thread = threading.Thread(target=executor_callback, daemon=True)
    thread.start()
    return nodes


#Wrapper to be able to quickly stop the thread
def executor_callback():
    global stop_flag, executor
    while not stop_flag:
        executor.spin_once()
    print(stop_flag)

#Restart the executor, needs to be done when modifying any attribute of a drone
def executor_restart():
    global executor, thread, stop_flag
    stop_flag = True
    thread.join()
    stop_flag = False

    thread = threading.Thread(target=executor_callback, daemon=True)
    thread.start()

#End the executor, stops all drones
def drone_clean():
    global executor
    executor.shutdown()

#move all drones within the nodes array to (x, y, z) in local coordinate system
def move_all_drones(nodes, x, y, z):
    for node in nodes:
        node.moveto(x, y, z)
    executor_restart()

def move_drones(nodes, coords):
    for node, coord in zip(nodes, coords):
        node.moveto(coord[0], coord[1], coord[2])
    executor_restart()

#Return the global position of all drones within the nodes array
def get_all_global_pos(nodes):
    positions = []
    for node in nodes:
        position = node.global_pos()
        positions.append(position)

    return positions

#Return the local position of all drones within the nodes array
def get_all_local_pos(nodes):
    positions = []
    for node in nodes:
        position = node.local_pos()
        positions.append(position)

    return positions


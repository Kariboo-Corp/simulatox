# Back README.md

<aside>
<img src="https://www.notion.so/icons/exclamation-mark_red.svg" alt="https://www.notion.so/icons/exclamation-mark_red.svg" width="40px" /> The following documentation assume that you’ve read the Dash documentation

</aside>

## Back-end operating

The main file `[app.py](http://app.py)` is working directly with **Dash** of the front. The method `setup` is setting up all the **callbacks** needed by the front-end to deal with the app logics. As the web app is for now pretty small all the callbakcs are specified directly in the `app.py` but later it would be smart to make multiples files.

This back-end is meant to be a graphic interface to accompany one user into dealing with drone swarms. It will typically embed scripts and macros to define new features that will be launchable through the front-end.  

This backend uses :

- ROS’ python package : [rclpy](https://github.com/ros2/rclpy) to implement all the functions used to communicate with PX4’s nodes.
- [px4_msgs](https://github.com/PX4/px4_msgs) to retrieve the proper format allowed through [MicroXRCEAgent](https://github.com/eProsima/Micro-XRCE-DDS-Agent?tab=readme-ov-file)

The file `launch.sh` within the commands folder gives an example of a script that can be used to launch PX4-Autopilot with multiples drones. Please note that MicroXRCEAgent must be running before launching PX4. 

<aside>
ℹ️ More informations regarding multiple-vehicle simulation can be found [here](https://docs.px4.io/main/en/sim_gazebo_gz/multi_vehicle_simulation.html)

</aside>

The file `control.py` within the commands folder implements a new node **OffboardControl**, along with few methods that can be used to communicate with **PX4**.

You can easily create a new kinds of node from this example, please note however :

- The **Quality of Service (QoS)** policies must **match** the policies of **PX4**. The default config for PX4’s QoS is the one given in OffboardControl. Modifying any policies might lead PX4 to refuse the message.
- The **publisher** and **subscribers** must be initialized when the node is instancied. You can find the list of accessible topics when **MicroXRCEAgent** and **PX4** are running with the command :

```bash
ros2 topic list
```

- In order to publish messages in a topic, a timer must be used.
- The attributs within a node object are only updated when the [`spin`](https://docs.ros2.org/foxy/api/rclpy/api/init_shutdown.html#rclpy.spin) or the [`spin_once`](https://docs.ros2.org/foxy/api/rclpy/api/init_shutdown.html#rclpy.spin_once) method is called

In order to use a single node, the [`spin`](https://docs.ros2.org/foxy/api/rclpy/api/init_shutdown.html#rclpy.spin) method of rclpy can be used.

Alternatively, the [`spin_once`](https://docs.ros2.org/foxy/api/rclpy/api/init_shutdown.html#rclpy.spin_once) method can be used.

In order to control multiples nodes at once, an [`executor`](https://docs.ros2.org/foxy/api/rclpy/api/execution_and_callbacks.html#module-rclpy.executors) must be created, containing all the nodes to control. The previous methods can be used on the executor

When trying to change an attribut used to be published into a topic, it is recommended to restart the executor.

Multiples functions are given to easily set up the nodes and executor when working with multiples drones ( namely : `drone_init`, `drone_clean`, `executor_restart`)

To understand in depth how PX4, ROS, Gazebo and uXRCE work altogether, the official documentation will be your best friend. Here are some links toward information you may need :

[uXRCE documentation](https://docs.px4.io/main/en/middleware/uxrce_dds.html)

[ROS humble documentation](https://docs.ros.org/en/humble/Tutorials.html)

[How to link PX4 and Gazebo](https://docs.px4.io/main/en/sim_gazebo_gz/)

[How to link PX4 and ROS](https://docs.px4.io/main/en/ros/ros2_comm.html#humble)
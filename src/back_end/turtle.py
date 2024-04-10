import subprocess
def launch_turtlesim():
    subprocess.Popen(['ros2', 'run', 'turtlesim', 'turtlesim_node'])

import signal
import os;
import subprocess

import back_end.commands.control as c
import rclpy;
process = None

def launch_sim(drone_number, drone_type="gz_x500"):
    #Exec ./commands/launch.sh
    global process
    process = subprocess.Popen(["./back_end/commands/launch.sh",str(drone_number), drone_type], stdout=subprocess.PIPE)
    print("Simulation Launched with PID: ", process.pid)
    try:
        rclpy.init()
    except:
        print("RCLPY already initialized")
def kill_sim():
    #Exec ./commands/kill.sh
    global process
    if process != None:
        print("Killing Simulation with PID: ", process.pid)
        #Pkill px4 and ruby
        os.system("pkill px4")
        os.system("pkill ruby")
        os.system("pkill launch.sh")
        
        
        os.kill(process.pid, signal.SIGKILL)

def init_drone(drone_number):
    return c.drone_init(drone_number)

def clean_drone():
    try:
        c.drone_clean()
    except:
        print("Executor already shutdown")
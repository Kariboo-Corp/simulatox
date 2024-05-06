import signal
import os;
import subprocess

process = None

def launch_sim(drone_number, drone_type="gz_x500"):
    #Exec ./commands/launch.sh
    global process
    process = subprocess.Popen(["./back_end/commands/launch.sh",str(drone_number), drone_type], stdout=subprocess.PIPE)
    print("Simulation Launched with PID: ", process.pid)
    
def kill_sim():
    #Exec ./commands/kill.sh
    global process
    if process != None:
        print("Killing Simulation with PID: ", process.pid)
        #Pkill px4 and ruby
        os.system("pkill px4")
        os.system("pkill ruby")
        
        os.kill(process.pid, signal.SIGKILL)


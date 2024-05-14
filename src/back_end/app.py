import back_end.general as g
import back_end.commander as commander
import back_end.commands.control as c
import front_end.modules as m
import dash as d
import time
import threading


## Global Variables
is_simulation_running = False
drone_number = 1
drones = []
## Drone Movement
selected_drone_id=1;
x, y, z = 0, 0, 0


##TOOLS
simulation_running_txt = lambda txt :"Simulation Start"  if is_simulation_running else txt
not_simulation_running_txt = lambda txt :"Simulation Stop" if not is_simulation_running else txt

def get_drone_data():
    global drones
    drone_data = {}
    for i in range(len(drones)):
        drone : c.OffboardControl = drones[i]
        drone_data.update({drone.id :drone.local_pos()})
    return drone_data

def setup(app : d.Dash):

    ################SIMULATION################

    ##Setting Start Button CallBack
    @app.callback(
        [d.Output("start", "children"), d.Output("start", "disabled", allow_duplicate=True), d.Output("stop", "disabled", allow_duplicate=True)],
        [d.Input("start", "n_clicks")], 
        prevent_initial_call=True
    )
    def start_simulation(n_clicks):
        global drones, drone_number, is_simulation_running
        if is_simulation_running:
            return simulation_running_txt("Start Simulation"), is_simulation_running, not is_simulation_running
        g.launch_sim(drone_number)
        is_simulation_running = True
        print("Simulation Started with ",drone_number, "drone")
        return simulation_running_txt("Start Simulation"),  is_simulation_running, not is_simulation_running
    ##Setting drone_number Input CallBack
    @app.callback(
        d.Output("num_drone", "value"),
        [d.Input("num_drone", "value")],
        prevent_initial_call=True
    )
    def update_drone_number(value):
        global drone_number
        drone_number = value
        return drone_number


    ##Setting stop Button CallBack
    @app.callback(
        [d.Output("stop", "children"), d.Output("start", "disabled", allow_duplicate=True), d.Output("stop", "disabled", allow_duplicate=True)],
        [d.Input("stop", "n_clicks")],
        prevent_initial_call=True
    )
    def stop_simulation(n_clicks):
        global drones, is_simulation_running
        if not is_simulation_running:
            return not_simulation_running_txt("Stop Simulation"), is_simulation_running, not is_simulation_running
        g.kill_sim()
        is_simulation_running = False
        print("Simulation Stopped", is_simulation_running)
        drones = []
        g.clean_drone()
        return not_simulation_running_txt("Stop Simulation"), is_simulation_running, not is_simulation_running
    ################SIMULATION################

    ################MOVE DRONE################
    ##Set Button Card
    @app.callback(
        d.Output("move", "n_clicks"),
        [d.Input("move", "n_clicks")],
        prevent_initial_call=True
    )
    def move_drone(n_clicks):
        global drones
        if len(drones)==0:
            drones  = g.init_drone(drone_number)
        global x,y,z
        print("Moving Drone")
        job = threading.Thread(target=commander.move, args=(x,y,z,drones[selected_drone_id-1]))
        job.start()
        return n_clicks
    
    ##Set Drone ID with value
    @app.callback(
        d.Output("drone_id", "value"),
        [d.Input("drone_id", "value")],
        prevent_initial_call=True
    )
    def update_drone_id(value):
        global selected_drone_id
        selected_drone_id = value
        return selected_drone_id

    ##Set Drone vector (id = x,y,z) with value
    @app.callback(
        [d.Output("x", "value"), d.Output("y", "value"), d.Output("z", "value")],
        [d.Input("x", "value"), d.Input("y", "value"), d.Input("z", "value")],
        prevent_initial_call=True
    )
    def update_drone_vector(xin, yin, zin):
        global x,y,z
        x = xin
        y = yin
        z = zin
        return x, y, z

    ################MOVE DRONE################


    ################ARM ALL DRONE################
    ##Set Button Card
    @app.callback(
        d.Output("arm_all", "n_clicks"),
        [d.Input("arm_all", "n_clicks")],
        prevent_initial_call=True
    )
    def arm_all_drone(n_clicks):
        global drones
        if len(drones)==0:
            drones  = g.init_drone(drone_number)
        print("Arm All Drone")
        job = threading.Thread(target=commander.arm_all_drones, args=(drones,))
        job.start()
        return n_clicks



    ################DRONE LIST################
    ##Set Drone List
    @app.callback(
        d.Output("drone_list", "children"),
        [d.Input("update", "n_intervals")]
    )
    def update_drone_list(n_intervals):
        data = get_drone_data()
        drone_list = []
        for key in data:
            drone_list.append(m.makeDroneCard(key, data[key]))
        return drone_list
    ################DRONE LIST################
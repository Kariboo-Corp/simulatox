import back_end.general as g
import back_end.commander as commander
import dash as d

## Global Variables
is_simulation_running = False
drone_number = 1

## Drone Movement
selected_drone_id=1;
x, y, z = 0, 0, 0

def linkBackToFront(app : d.Dash):
    ##Setting Start Button CallBack
    @app.callback(
        [d.Output("start", "children"), d.Output("start", "disabled", allow_duplicate=True), d.Output("stop", "disabled", allow_duplicate=True)],
        [d.Input("start", "n_clicks")],
        prevent_initial_call=True   
    )
    def start_simulation(n_clicks):
        g.launch_sim(drone_number)
        is_simulation_running = True
        print("Simulation Started")
        return "Simulation Started", is_simulation_running, not is_simulation_running

    ##Setting drone_number Input CallBack
    @app.callback(
        d.Output("num_drone", "value"),
        [d.Input("num_drone", "value")],
        prevent_initial_call=True
    )
    def update_drone_number(value):
        drone_number = value
        return drone_number


    ##Setting stop Button CallBack
    @app.callback(
        [d.Output("stop", "children"), d.Output("start", "disabled", allow_duplicate=True), d.Output("stop", "disabled", allow_duplicate=True)],
        [d.Input("stop", "n_clicks")],
        prevent_initial_call=True
    )
    def stop_simulation(n_clicks):
        g.kill_sim()
        is_simulation_running = False
        print("Simulation Stopped")

        return "Simulation Stopped", is_simulation_running, not is_simulation_running
    

    ##Set Move Drone Card

    ##Set Button Card
    @app.callback(
        d.Output("move", "n_clicks"),
        [d.Input("move", "n_clicks")],
        prevent_initial_call=True
    )
    def move_drone(n_clicks):
        print("Moving Drone")
        commander.move(x,y,z,selected_drone_id)
        return n_clicks
    
    ##Set Drone ID with value
    @app.callback(
        d.Output("drone_id", "value"),
        [d.Input("drone_id", "value")],
        prevent_initial_call=True
    )
    def update_drone_id(value):
        selected_drone_id = value
        return selected_drone_id

    ##Set Drone vector (id = x,y,z) with value
    @app.callback(
        [d.Output("x", "value"), d.Output("y", "value"), d.Output("z", "value")],
        [d.Input("x", "value"), d.Input("y", "value"), d.Input("z", "value")],
        prevent_initial_call=True
    )
    def update_drone_vector(xin, yin, zin):
        x = xin
        y = yin
        z = zin
        return x, y, z



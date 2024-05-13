import dash as d
import dash_bootstrap_components as dbc

def makeDroneCard(drone_id, drone_coord):
    return dbc.Col(dbc.Card(dbc.CardBody([
        d.html.H1(f"Drone {drone_id}"),
        d.html.P(f"Coordinates: x:{round(drone_coord[0],2)}, y:{round(drone_coord[2]*-1,2)}, z:{round(drone_coord[1],2)}"),
    ])))
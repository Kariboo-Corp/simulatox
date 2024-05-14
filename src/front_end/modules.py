import dash as d
import dash_bootstrap_components as dbc

def makeDroneCard(drone_id, drone_coord):
    return dbc.Col(dbc.Card(dbc.CardBody([
        dbc.CardHeader(f"Drone {drone_id}"),
        dbc.Row([
            dbc.Col(dbc.CardImg(src="assets/x500.png", top=True, style={"width":"50px"}),width=2),
            dbc.Col(d.html.P(f"Coordinates: x:{round(drone_coord[0],2)}, y:{round(drone_coord[2]*-1,2)}, z:{round(drone_coord[1],2)}")),
       ])
    ])))
import dash as d
import dash_bootstrap_components as dbc


app = d.Dash(name="Simulatox",title="Simulatox",external_stylesheets=[dbc.themes.BOOTSTRAP])



app.layout = d.html.Div([
    d.dcc.Store(id="drone_data",data={}),
    d.dcc.Interval(id="update",interval=2*1000,n_intervals=0),
    dbc.Card(dbc.CardBody([
        d.html.H1("Start Simulation"),
        #Ask for number of drone
        dbc.Row(
        [
            dbc.Col(dbc.Label("Enter number of drone"), width=2),
            dbc.Col(dbc.Input(placeholder="Enter number of drone", type="number", id="num_drone",value=1),width=2)
        ],align="start",justify="start"),
        dbc.Row([
            dbc.Col(dbc.Button("Start Simulation", color="primary", id="start"),width=2),
            dbc.Col(dbc.Button("Stop Simulation", color="danger", id="stop"), width=2)
        ], align="start"),
    ])),
    dbc.Card(dbc.CardBody([
        d.html.H1("Move Drone"),
        #Ask for drone id
        dbc.Row(
        [
            dbc.Col(dbc.Label("Selected drone id"), width=2),
            dbc.Col(dbc.Input(placeholder="Enter drone id", type="number", id="drone_id", value=1),width=2)
        ]),
        #Ask for vector
        dbc.Row([
            dbc.Col(dbc.Label("X:"), width=1, align="center",class_name="text-center"),
            dbc.Col(dbc.Input(placeholder="Enter x", type="number", id="x", value=0),width=2),
            dbc.Col(dbc.Label("Y:"), width=1, align="center",class_name="text-center"),
            dbc.Col(dbc.Input(placeholder="Enter y", type="number", id="y",value=0),width=2),
            dbc.Col(dbc.Label("Z:"), width=1, align="center",class_name="text-center"),
            dbc.Col(dbc.Input(placeholder="Enter z", type="number", id="z",value=0),width=2)
        ], align="start"),
        dbc.Row([
            dbc.Col(dbc.Button("Move Drone", color="primary", id="move"),width=2),
            dbc.Col(dbc.Button("Arm All Drones", color="primary", id="arm_all"), width=2)

        ])
    ])),
    dbc.Card(dbc.CardBody(dbc.Row(id="drone_list")))
])


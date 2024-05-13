import dash as d
import dash_bootstrap_components as dbc


app = d.Dash(name="Simulatox",title="Simulatox",external_stylesheets=[dbc.themes.BOOTSTRAP])



app.layout = d.html.Div([
    d.dcc.Store(id="drone_data",data={}),
    d.dcc.Interval(id="update",interval=2*1000,n_intervals=0),
    dbc.Card(dbc.CardBody([
        d.html.H1("Start Simulation"),
        #Ask for number of drone
        dbc.Input(placeholder="Enter number of drone", type="number", id="num_drone",value=1),
        dbc.Row([
            dbc.Col(dbc.Button("Start Simulation", color="primary", id="start")),
            dbc.Col(dbc.Button("Stop Simulation", color="danger", id="stop"))
        ], align="start"),
    ])),
    dbc.Card(dbc.CardBody([
        d.html.H1("Move Drone"),
        #Ask for drone id
        dbc.Input(placeholder="Enter drone id", type="number", id="drone_id", value=1),
        #Ask for vector
        dbc.Row([
            dbc.Col(dbc.Input(placeholder="Enter x", type="number", id="x", value=0)),
            dbc.Col(dbc.Input(placeholder="Enter y", type="number", id="y",value=0)),
            dbc.Col(dbc.Input(placeholder="Enter z", type="number", id="z",value=0))
        ], align="start"),
        dbc.Button("Move Drone", color="primary", id="move")

    ])),
    dbc.Card(dbc.CardBody(dbc.Row(id="drone_list")))
])


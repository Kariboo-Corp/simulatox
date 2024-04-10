import dash as d
import dash_bootstrap_components as dbc

app = d.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = d.html.Div([
    dbc.Card(dbc.CardBody(dbc.Button("Test Boutton", color="info", className="mr-1", id="test_button")))
])


def setCallbackButton(callback):
    @app.callback(
        d.Output("test_button", "children"),
        [d.Input("test_button", "n_clicks")],
        prevent_initial_call=True
        
    )
    def update_output(n_clicks):
        return callback(n_clicks)


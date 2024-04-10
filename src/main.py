from front_end.app import app, setCallbackButton
from back_end.turtle import launch_turtlesim

setCallbackButton(lambda n_clicks: launch_turtlesim())

app.run_server(debug=True, port=8000,host="0.0.0.0")


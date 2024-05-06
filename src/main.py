from front_end.app import app
from back_end.app import linkBackToFront


linkBackToFront(app);
app.run_server(debug=True, port=8000,host="0.0.0.0")


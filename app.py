# Imports
from flask import Flask, render_template
from controllers.player_controller import player_controller

# App. Creates an instance of flask-app object
flaskApp = Flask(__name__) # Handles HTTP-requests
flaskApp.register_blueprint(player_controller)

# Route for index
@flaskApp.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    flaskApp.run(debug=True)
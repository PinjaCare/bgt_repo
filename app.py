# Imports
from flask import Flask, render_template
from controllers.player_controller import player_controller
from controllers.games_controller import games_controller
from controllers.session_controller import session_controller

# App. Creates an instance of flask-app object
flaskApp = Flask(__name__) # Handles HTTP-requests

# Blueprints for controllers:
flaskApp.register_blueprint(player_controller)
flaskApp.register_blueprint(games_controller)
flaskApp.register_blueprint(session_controller)

# Route for index
@flaskApp.route("/")
def index(): # Renders index
    return render_template("index.html")

if __name__ == "__main__":
    flaskApp.run(debug=True)
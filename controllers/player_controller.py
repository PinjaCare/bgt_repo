from flask import Blueprint, render_template, request, redirect
from database import get_db_connection
from models.player import Player

player_controller = Blueprint("player_controller", __name__)

# Route for players
@player_controller.route("/players") # Method is GET by default unless stated otherwise
def get_players():
    connection = get_db_connection()
    players_from_db = connection.execute("SELECT * FROM players").fetchall()
    connection.close()

    player_list = [Player(row) for row in players_from_db]

    return render_template("players.html", players=player_list)


# Route for add player
@player_controller.route("/add_player", methods=["GET","POST"])
def add_player():
    if request.method == "POST":
        # Saving player's info to database if request method was POST
        name = request.form["player_name"]
        connection = get_db_connection()
        connection.execute(
            "INSERT INTO players (name) VALUES (?)", # Games played and wins are 0 by default in SQLlite.
            (name,)
        )
        connection.commit()
        connection.close()
        # Saving is ready and app redirects to URL /players
        return redirect("/players")
    # renders the template for adding players if request method was GET
    return render_template("add_player.html")

# Route for deleting player
@player_controller.route("/delete_player/<int:id>")
def delete_player(id):
    connection = get_db_connection()
    connection.execute("DELETE FROM players WHERE id = ?", (id,))
    connection.commit()
    connection.close()
    return redirect("/players")

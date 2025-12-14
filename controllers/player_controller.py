from flask import Blueprint, render_template, request, redirect, Response
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
    # Filtering order
    order = request.args.get("order","desc")
    # Sorting players by ranking with given order
    player_list_sorted = sorted(player_list, key=lambda p:p.ranking, reverse=( order == "desc" ))

    return render_template("players.html", players = player_list_sorted, selected_order = order)


# Route for adding player
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
        connection.commit() # Saves the changes in the database
        connection.close() # Closes the connection between server and the database.
        # Saving is finished and app redirects to URL /players
        return redirect("/players")
    # Renders the template for adding players if request method was GET
    return render_template("add_player.html")

# Route for deleting player
@player_controller.route("/delete_player/<int:id>", methods=["POST"])
def delete_player(id):
    connection = get_db_connection()
    connection.execute("DELETE FROM players WHERE id = ?", (id,))
    connection.commit()
    connection.close()
    return redirect("/players")

# Route for editing player
@player_controller.route("/edit_player/<int:id>", methods=["GET","POST"])
def edit_player(id):
    connection = get_db_connection()
    if request.method == "POST": # Editing player's info in the database if request method was POST
        name = request.form["player_name"]
        games = request.form["games_played"]
        wins = request.form["wins"]
        connection.execute("UPDATE players SET name = ?, games_played = ?, wins = ? WHERE id = ?", (name, games, wins, id))
        connection.commit()
        connection.close()
        return redirect("/players")

    player_to_be_edited = connection.execute("SELECT * FROM players WHERE id = ?", (id,)).fetchone() # Fetches only one player with the given id, if there isn't a player with that id, then this method returns None
    connection.close()
    if player_to_be_edited is None: # Checks if the player was found
        return Response("Player not found", status=404) # This status code indicates that server cannot find the requested resource, that is when the selected player didn't exist.
    player_object = Player(player_to_be_edited) # Player was found and this changes the fetched data to a player object
    return render_template("edit_player.html", player = player_object) # Selected player exists and will be forwarded to view



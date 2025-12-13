from flask import Blueprint, render_template, request, redirect, Response
from database import get_db_connection
from models.game import Game
from datetime import datetime

games_controller = Blueprint("games_controller", __name__)

# Route for listing games
@games_controller.route("/games") # Method is GET by default unless stated otherwise
def get_games():
    connection = get_db_connection()
    games_from_db = connection.execute("SELECT * FROM games").fetchall()
    connection.close()

    games_list = [Game(row) for row in games_from_db]

    return render_template("games.html", games=games_list)

# Route for adding game
@games_controller.route("/add_game", methods=["GET","POST"])
def add_game():
    if request.method == "POST":
        # Saving new game's info to database if request method was POST
        name = request.form["game_name"]
        genre = request.form["genre"]
        rating = float(request.form["rating"])
        min_players = request.form["min_players"]
        max_players = request.form["max_players"]
        last_updated = datetime.today().strftime("%Y-%m-%d")
        connection = get_db_connection()
        connection.execute(
            "INSERT INTO games (name, genre, rating, min_players, max_players, last_updated) VALUES (?,?,?,?,?,?)",
            (name, genre, rating, min_players, max_players, last_updated)
        )
        connection.commit() # Saves the changes in the database
        connection.close() # Closes the connection between server and the database.
        # Saving is finished and app redirects to URL /games
        return redirect("/games")
    # Renders the template for adding games if request method was GET
    return render_template("add_game.html")

# Route for deleting game
@games_controller.route("/delete_game/<int:id>", methods=["POST"])
def delete_game(id):
    connection = get_db_connection()
    connection.execute("DELETE FROM games WHERE id = ?", (id,))
    connection.commit()
    connection.close()
    return redirect("/games")

# Route for editing game
@games_controller.route("/edit_game/<int:id>", methods=["GET","POST"])
def edit_game(id):
    connection = get_db_connection()
    if request.method == "POST": # Editing data in the database if request method was POST
        name = request.form["game_name"]
        genre = request.form["genre"]
        rating = float(request.form["rating"])
        min_players = request.form["min_players"]
        max_players = request.form["max_players"]
        last_updated = datetime.today().strftime("%Y-%m-%d")
        connection.execute("UPDATE games SET name = ?, genre = ?, rating = ?, min_players = ?, max_players = ?, last_updated = ? WHERE id = ?",
                           (name, genre, rating, min_players, max_players, last_updated, id))
        connection.commit()
        connection.close()
        return redirect("/games")

    game_to_be_edited = connection.execute("SELECT * FROM games WHERE id = ?", (id,)).fetchone() # Fetches only one game with the given id, if that id doesn't exist, then this method returns None
    connection.close()
    if game_to_be_edited is None: # Checks if the game was found
        return Response("Game not found", status=404) # This status code indicates that server cannot find the requested resource, that is when the selected game didn't exist.
    game_object = Game(game_to_be_edited) # Game was found and this changes the fetched data to a game object
    return render_template("edit_game.html", game = game_object) # Game is forwarded to view
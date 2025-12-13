from flask import Blueprint, render_template, request, redirect, Response
from database import get_db_connection
from models.game import Game

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
        rating = request.form["rating"]
        min_players = request.form["min_players"]
        max_players = request.form["max_players"]
        last_updated = request.form["last_updated"]
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
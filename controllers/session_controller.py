from flask import Blueprint, render_template, request, redirect
from database import get_db_connection
from models.session import Session

session_controller = Blueprint("session_controller", __name__)

###########################################################################################
# LISTING SESSIONS
@session_controller.route("/sessions")
def get_sessions():
    connection = get_db_connection()

    player_id = request.args.get("player_id") # URL Queryn parameters

    # Fetch sessions (filtered or not)
    if player_id:
        sessions = connection.execute("""
            SELECT DISTINCT s.*
            FROM sessions s
            JOIN session_players sp ON sp.session_id = s.id
            WHERE sp.player_id = ?
            ORDER BY s.date_played DESC
        """, (player_id,)).fetchall()
    else:
        sessions = connection.execute("""
            SELECT s.*
            FROM sessions s
            ORDER BY s.date_played DESC
        """).fetchall()

    session_objects_list = []

    for session in sessions:
        session_id = session["id"]

        # Fetch participants
        participants = connection.execute("""
            SELECT p.name
            FROM session_players sp
            JOIN players p ON p.id = sp.player_id
            WHERE sp.session_id = ?
        """, (session_id,)).fetchall()
        participants_list = [r["name"] for r in participants]

        # Fetch winners
        winners = connection.execute("""
            SELECT p.name
            FROM session_winners sw
            JOIN players p ON p.id = sw.player_id
            WHERE sw.session_id = ?
        """, (session_id,)).fetchall()
        winners_list = [r["name"] for r in winners]

        session_obj = Session(
            session,
            game_name=session["game_name"],
            participants=participants_list,
            winners=winners_list
        )

        session_objects_list.append(session_obj)

    # Fetch players for filter dropdown
    players_list = connection.execute("SELECT * FROM players").fetchall()

    connection.close()

    return render_template(
        "sessions.html",
        sessions=session_objects_list,
        players=players_list,
        selected_player_id=player_id
    )

###########################################################################################
# ADDING SESSION
@session_controller.route("/add_session", methods=["GET", "POST"]) # /add_session is the HTTP route which accepts only GET and POST methods
def add_session():
    connection = get_db_connection() # Database connection

    if request.method == "POST": # User submits a form
        # Reading data from the form
        game_id = request.form["game_id"]
        duration = request.form["duration_minutes"]
        date_played = request.form["date_played"]
        participants = request.form.getlist("participants") # Data as list, comes from checkbox
        winners = request.form.getlist("winners") # Data as list, comes from checkbox

        # Fetching game name from games table for historical storage
        game = connection.execute(
            "SELECT name FROM games WHERE id = ?", # ? and tuples prevent SQL injection
            (game_id,)
        ).fetchone() # Returns single row

        # Inserts session with game_name stored
        cursor = connection.execute("""
            INSERT INTO sessions (game_id, game_name, duration_minutes, date_played)
            VALUES (?, ?, ?, ?)
        """, (game_id, game["name"], duration, date_played))

        new_session_id = cursor.lastrowid

        # Inserts participants
        for player_id in participants:
            connection.execute("""
                INSERT INTO session_players (session_id, player_id)
                VALUES (?, ?)
            """, (new_session_id, player_id))
            # Increments games_played
            connection.execute("""
                UPDATE players
                SET games_played = games_played + 1
                WHERE id = ?
            """, (player_id,))

        # Inserts winners
        for winner_id in winners:
            connection.execute("""
                INSERT INTO session_winners (session_id, player_id)
                VALUES (?, ?)
            """, (new_session_id, winner_id))
            # Increments wins
            connection.execute("""
                UPDATE players
                SET wins = wins + 1
                WHERE id = ?
            """, (winner_id,))

        connection.commit()
        connection.close()
        return redirect("/sessions")

    # GET request. User request to see the form.
    games_list = connection.execute("SELECT * FROM games").fetchall() # Games for dropdown selection
    players_list = connection.execute("SELECT * FROM players").fetchall() # Players for checkboxes 'participants' and 'winners'
    connection.close()

    # Shows form to the user. games and players are sent to HTML template for Jinja2 to use
    return render_template(
        "add_session.html",
        games=games_list,
        players=players_list
    )

###########################################################################################
# DELETING SESSION
@session_controller.route("/delete_session/<int:id>", methods=["POST"])
def delete_session(id):
    connection = get_db_connection()

    # Fetch participants
    participants = connection.execute("""
        SELECT player_id
        FROM session_players
        WHERE session_id = ?
    """, (id,)).fetchall()

    # Fetch winners
    winners = connection.execute("""
        SELECT player_id
        FROM session_winners
        WHERE session_id = ?
    """, (id,)).fetchall()

    # Rollback stats if player doesn't have 0 games played
    for row in participants:
        connection.execute("""
            UPDATE players
            SET games_played = CASE  
                WHEN games_played > 0 THEN games_played - 1
                ELSE 0
            END
            WHERE id = ?
        """, (row["player_id"],))
    # Rollback stats if player doesn't have 0 wins.
    for row in winners:
        connection.execute("""
            UPDATE players
            SET wins = CASE
                WHEN wins > 0 THEN wins - 1
                ELSE 0
            END
            WHERE id = ?
        """, (row["player_id"],))

    # Deletes row/rows from helper tables
    connection.execute("DELETE FROM session_players WHERE session_id = ?", (id,))
    connection.execute("DELETE FROM session_winners WHERE session_id = ?", (id,))

    # Deletes session
    connection.execute("DELETE FROM sessions WHERE id = ?", (id,))

    connection.commit() # Saves changes
    connection.close() # Closes connection to db
    return redirect("/sessions")
from flask import Blueprint, render_template, request, redirect, Response
from database import get_db_connection
from models.session import Session


session_controller = Blueprint("session_controller", __name__)

# LISTING SESSIONS
###########################################################################################
# Route for listing sessions
@session_controller.route("/sessions") # Method is GET by default unless stated otherwise
def get_sessions():
    connection = get_db_connection()

    # Fetching all sessions with game names
    sessions = connection.execute("""
        SELECT s.*, g.name AS game_name
        FROM sessions s
        JOIN games g ON g.id = s.game_id
        ORDER BY s.date_played DESC
    """).fetchall()

    session_objects_list = []

    for session in sessions:
        session_id = session["id"]

        # Fetching participant names
        participants = connection.execute("""
            SELECT p.name FROM session_players sp
            JOIN players p ON p.id = sp.player_id
            WHERE sp.session_id = ?
        """, (session_id,)).fetchall()
        participants_list = [r["name"] for r in participants]

        # Fetching winner names
        winners = connection.execute("""
            SELECT p.name FROM session_winners sw 
            JOIN players p ON p.id = sw.player_id 
            WHERE sw.session_id = ?
        """, (session_id,)).fetchall()
        winners_list = [r["name"] for r in winners]

        # Creating Session-obj
        session_obj = Session(
            session,
            game_name=session["game_name"],
            participants=participants_list,
            winners=winners_list
        )

        session_objects_list.append(session_obj)

    connection.close()

    return render_template("sessions.html", sessions=session_objects_list)

#################################################################################################
# ADDING SESSION
@session_controller.route("/add_session", methods=["GET","POST"])
def add_session():
    connection = get_db_connection()
    if request.method == "POST":
        # Collects data from forms in add_session view
        game_id = request.form["game_id"]
        duration = request.form["duration_minutes"]
        date_played = request.form["date_played"]
        participants = request.form.getlist("participants")
        winners = request.form.getlist("winners")
        # New session to sessions-board
        cursor = connection.execute("""
            INSERT INTO sessions (game_id, duration_minutes, date_played) VALUES (?,?,?)
        """, (game_id,duration,date_played))

        new_session_id = cursor.lastrowid

        # New session's participant(s) to session_players-board
        for player_id in participants:
            connection.execute("""
                INSERT INTO session_players (session_id, player_id) VALUES (?,?)
        """, (new_session_id, player_id))

        # New session's winner(s)
        for winner_id in winners:
            connection.execute("""
                INSERT INTO session_winners (session_id, player_id) VALUES (?,?)    
        """, (new_session_id, winner_id))

        connection.commit()
        connection.close()
        return  redirect("/sessions")

    # If request method was GET
    games_list = connection.execute("SELECT * FROM games").fetchall()
    players_list = connection.execute("SELECT * FROM players").fetchall()
    connection.close()
    return render_template("add_session.html", games=games_list, players=players_list)
######################################################################################################
# DELETING SESSION

























from flask import Blueprint, render_template, request, redirect, Response
from database import get_db_connection
from models.session import Session


session_controller = Blueprint("session_controller", __name__)

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

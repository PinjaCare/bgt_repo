class Session:
    def __init__(self, row, game_name=None, participants=None, winners=None):
        self.id = row["id"]
        self.game_id = row["game_id"]
        self.duration_minutes = row["duration_minutes"]
        self.date_played = row["date_played"]

        self.game_name = game_name
        self.participants = participants or []
        self.winners = winners or []
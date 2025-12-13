class Session:
    def __init__(self, row):
        self.id = row["id"]
        self.game_id = row["game_id"]
        self.duration = row["duration"]
        self.winner_id = row["winner_id"]
        self.date_played = row["date_played"]
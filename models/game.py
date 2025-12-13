class Game:
    def __init__(self, row):
        self.id = row["id"]
        self.name = row["name"]
        self.genre = row["genre"]
        self.rating = row["rating"]
        self.min_players = row["min_players"]
        self.max_players = row["max_players"]
        self.last_updated = row["last_updated"]

    @property
    def ideal_participants_range(self):
        return f"{self.min_players}-{self.max_players}"

class Player:
    def __init__(self, row):
        self.id = row["id"]
        self.name = row["name"]
        self.games_played = row["games_played"]
        self.wins = row["wins"]

    @property
    def ranking(self):
        if self.games_played == 0:
            return 0
        return round((self.wins/self.games_played) * 100, 1)
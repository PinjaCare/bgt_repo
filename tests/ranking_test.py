from models.player import Player

# 2/3 should succeed and one should fail

######## Should succeed ###############

def test_ranking_is_50():
    player_row = {
        "id" : 1,
        "name" : "test_player",
        "games_played" : 2,
        "wins" : 1
    }
    new_player = Player(player_row)
    assert new_player.ranking == 50.0

def test_ranking_is_0():
    player_row = {
        "id" : 2,
        "name" : "test_player_no_games",
        "games_played" : 0,
        "wins" : 0
    }
    new_player = Player(player_row)

    assert new_player.ranking == 0

########### Should fail #################

def test_ranking_is_0_fail():
    player_row = {
        "id" : 3,
        "name" : "test_player2",
        "games_played" : 1,
        "wins" : 1
    }
    new_player = Player(player_row)

    assert new_player.ranking == 0
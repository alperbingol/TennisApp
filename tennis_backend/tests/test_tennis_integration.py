from fastapi.testclient import TestClient
from tennis_backend.main import app

client = TestClient(app)

def test_basic_score_progression():
    """Test the basic tennis scoring: 0 → 15 → 30 → 40"""
    
    # Start: Alcaraz should be at 0
    response = client.get("/players/Alcaraz")
    assert response.json()["points"] == 0
    
    # First point: 0 → 15
    client.post("/players/Alcaraz/increment")
    response = client.get("/players/Alcaraz")
    assert response.json()["points"] == 15
    
    # Second point: 15 → 30
    client.post("/players/Alcaraz/increment")
    response = client.get("/players/Alcaraz")
    assert response.json()["points"] == 30
    
    # Third point: 30 → 40
    client.post("/players/Alcaraz/increment")
    response = client.get("/players/Alcaraz")
    assert response.json()["points"] == 40
    
    print("✅ Basic scoring progression works correctly!")

def test_win_game_from_40():
    """Test winning a game: 40 → win (points reset to 0, games increase by 1)"""
    
    # Get Alcaraz to 40 points
    for _ in range(3):  # 0→15→30→40
        client.post("/players/Alcaraz/increment")
    
    # Verify at 40
    response = client.get("/players/Alcaraz")
    player_data = response.json()
    assert player_data["points"] == 40
    assert player_data["current_set_games"] == 0
    
    # Win the game: 40 → win
    client.post("/players/Alcaraz/increment")
    
    # Check the results
    response = client.get("/players/Alcaraz")
    player_data = response.json()
    
    print(f"After winning game - Points: {player_data['points']}, Games: {player_data['current_set_games']}")
    
    assert player_data["points"] == 0           # Points should reset
    assert player_data["current_set_games"] == 1  # Games should increase

def test_deuce_scenario():
    """Test deuce: when both players reach 40, next point gives advantage"""
    
    # Get both players to 40 (deuce situation)
    for _ in range(3):  # Both to 40
        client.post("/players/Alcaraz/increment")
        client.post("/players/Sinner/increment")
    
    # Verify both at 40
    alcaraz = client.get("/players/Alcaraz").json()
    sinner = client.get("/players/Sinner").json()
    
    print(f"Before advantage - Alcaraz: {alcaraz['points']}, Sinner: {sinner['points']}")
    assert alcaraz["points"] == 40
    assert sinner["points"] == 40
    assert alcaraz["advantage"] == False
    assert sinner["advantage"] == False
    
    # Alcaraz wins next point → should get advantage
    client.post("/players/Alcaraz/increment")
    
    alcaraz = client.get("/players/Alcaraz").json()
    sinner = client.get("/players/Sinner").json()
    
    print(f"After advantage - Alcaraz advantage: {alcaraz['advantage']}, Sinner advantage: {sinner['advantage']}")
    
    assert alcaraz["advantage"] == True   # Alcaraz has advantage
    assert sinner["advantage"] == False   # Sinner doesn't

def test_advantage_to_win_game():
    """Test: Advantage + win point = win the game"""
    
    # Set up deuce (both at 40)
    for _ in range(3):
        client.post("/players/Alcaraz/increment")
        client.post("/players/Sinner/increment")
    
    # Alcaraz gets advantage
    client.post("/players/Alcaraz/increment")
    
    # Verify advantage
    alcaraz = client.get("/players/Alcaraz").json()
    assert alcaraz["advantage"] == True
    assert alcaraz["current_set_games"] == 0  # No game won yet
    
    # Alcaraz wins the next point → should win the game
    client.post("/players/Alcaraz/increment")
    
    alcaraz = client.get("/players/Alcaraz").json()
    print(f"After winning from advantage - Points: {alcaraz['points']}, Games: {alcaraz['current_set_games']}, Advantage: {alcaraz['advantage']}")
    
    assert alcaraz["points"] == 0           # Points reset
    assert alcaraz["current_set_games"] == 1  # Won the game
    assert alcaraz["advantage"] == False    # Advantage cleared

def test_advantage_back_to_deuce():
    """Test: Advantage + lose point = back to deuce"""

    # Set up deuce (both at 40)
    for _ in range(3):
        client.post("/players/Alcaraz/increment")
        client.post("/players/Sinner/increment")
    
    # Alcaraz gets advantage
    client.post("/players/Alcaraz/increment")

    # Verify advantage
    alcaraz = client.get("/players/Alcaraz").json()
    assert alcaraz["advantage"] == True
    assert alcaraz["current_set_games"] == 0  # No game won yet

    # Sinner wins the next point → deuce
    client.post("/players/Sinner/increment")

    alcaraz = client.get("/players/Alcaraz").json()
    sinner =  client.get("/players/Sinner").json()

    print(f"Back to deuce - Alcaraz points: {alcaraz['points']}, Games: {alcaraz['current_set_games']}, Advantage: {alcaraz['advantage']}, Sinner points: {sinner['points']}, Games: {sinner['current_set_games']}, Advantage: {sinner['advantage']} ")

    assert alcaraz["points"] == 40           # Still at 40
    assert alcaraz["advantage"] == False    # Advantage lost

    assert sinner["points"] == 40           # Still at 40
    assert sinner["advantage"] == False    # Advantage lost

def test_set_win_6_0():
    """Test winning a set 6-0 (6 games to 0)"""
    
    # Win 6 games in a row for Alcaraz
    for game in range(6):
        # Win 4 points per game (0→15→30→40→win)
        for point in range(4):
            client.post("/players/Alcaraz/increment")
        
        # Check games after each game win
        alcaraz = client.get("/players/Alcaraz").json()
        print(f"After game {game + 1}: Alcaraz has {alcaraz['current_set_games']} games")
    
    # After 6 games, should win the set
    alcaraz = client.get("/players/Alcaraz").json()
    sinner = client.get("/players/Sinner").json()
    
    print(f"Final - Alcaraz sets: {alcaraz['sets']}, games: {alcaraz['current_set_games']}")
    print(f"Final - Sinner sets: {sinner['sets']}, games: {sinner['current_set_games']}")
    
    # Set should be won and recorded
    assert len(alcaraz["sets"]) == 1        # Alcaraz has 1 completed set
    assert alcaraz["sets"][0] == 6          # Won 6 games in that set
    assert len(sinner["sets"]) == 1         # Sinner also has 1 completed set
    assert sinner["sets"][0] == 0           # Won 0 games in that set
    
    # Games should reset for next set
    assert alcaraz["current_set_games"] == 0
    assert sinner["current_set_games"] == 0

def test_tiebreak_triggered_at_6_6():
    """Test that tiebreak is triggered when both players reach 6 games"""
    
    # Get both players to 6 games each
    for game in range(6):
        # Alcaraz wins a game (4 points)
        for _ in range(4):
            client.post("/players/Alcaraz/increment")
        
        # Sinner wins a game (4 points)  
        for _ in range(4):
            client.post("/players/Sinner/increment")
    
    # Verify both at 6 games
    alcaraz = client.get("/players/Alcaraz").json()
    sinner = client.get("/players/Sinner").json()
    
    print(f"Before tiebreak - Alcaraz: {alcaraz['current_set_games']} games, Sinner: {sinner['current_set_games']} games")
    assert alcaraz["current_set_games"] == 6
    assert sinner["current_set_games"] == 6
    assert alcaraz["tiebreak"] == False  # Not in tiebreak yet
    
    # Next point should trigger tiebreak
    client.post("/players/Alcaraz/increment")
    
    alcaraz = client.get("/players/Alcaraz").json()
    sinner = client.get("/players/Sinner").json()
    
    print(f"After tiebreak trigger - Alcaraz tiebreak: {alcaraz['tiebreak']}, Sinner tiebreak: {sinner['tiebreak']}")
    print(f"Tiebreak points - Alcaraz: {alcaraz['tiebreak_points']}, Sinner: {sinner['tiebreak_points']}")
    
    assert alcaraz["tiebreak"] == True   # Both should be in tiebreak
    assert sinner["tiebreak"] == True
    assert alcaraz["tiebreak_points"] == 1  # Alcaraz should have 1 tiebreak point
    assert sinner["tiebreak_points"] == 0   # Sinner should have 0

def test_tiebreak_win():
    """Test winning a tiebreak 7-0"""
    
    # Set up 6-6 games and enter tiebreak
    for game in range(6):
        for _ in range(4):
            client.post("/players/Alcaraz/increment")
        for _ in range(4):
            client.post("/players/Sinner/increment")
    
    # Enter tiebreak (this gives Alcaraz first tiebreak point)
    client.post("/players/Alcaraz/increment")
    
    # Alcaraz wins 6 more tiebreak points (total 7)
    for _ in range(6):
        client.post("/players/Alcaraz/increment")
    
    # Check final result
    alcaraz = client.get("/players/Alcaraz").json()
    sinner = client.get("/players/Sinner").json()
    
    print(f"After tiebreak win - Alcaraz sets: {alcaraz['sets']}, Sinner sets: {sinner['sets']}")
    print(f"Current games - Alcaraz: {alcaraz['current_set_games']}, Sinner: {sinner['current_set_games']}")
    
    # Should win the set 7-6
    assert len(alcaraz["sets"]) == 1
    assert alcaraz["sets"][0] == 7        # Won 7-6 (6 games + tiebreak)
    assert sinner["sets"][0] == 6         # Lost 6-7
    
    # Should reset for next set
    assert alcaraz["current_set_games"] == 0
    assert sinner["current_set_games"] == 0
    assert alcaraz["tiebreak"] == False
    assert sinner["tiebreak"] == False

def test_match_win():
    """Test winning a match (first to 3 sets wins)"""
    
    # Simulate Alcaraz winning 3 sets quickly (3 x 6-0 sets)
    for set_num in range(3):
        print(f"Starting set {set_num + 1}")
        
        # Win 6 games per set (6-0)
        for game in range(6):
            for _ in range(4):  # 4 points per game
                client.post("/players/Alcaraz/increment")
    
    # Check match result
    alcaraz = client.get("/players/Alcaraz").json()
    sinner = client.get("/players/Sinner").json()
    
    print(f"Final - Alcaraz sets: {alcaraz['sets']}, winner: {alcaraz['winner']}")
    print(f"Final - Sinner sets: {sinner['sets']}, winner: {sinner['winner']}")
    
    assert len(alcaraz["sets"]) == 3      # Won 3 sets
    assert all(score == 6 for score in alcaraz["sets"])  # All 6-0
    assert len(sinner["sets"]) == 3       # Lost 3 sets  
    assert all(score == 0 for score in sinner["sets"])   # All 0-6
    
    assert alcaraz["winner"] == True      # Alcaraz wins match
    assert sinner["winner"] == False      # Sinner loses match
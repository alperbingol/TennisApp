import pytest
from main import players_data

import pytest
from main import players_data

#beforeEach

#afterEach

@pytest.fixture(autouse=True)
def reset_players_data():
    """Reset players data to clean state before each test"""
    print("🧹 Cleaning up data before test...")
    
    players_data.clear()
    players_data.update({
        "Alcaraz": {
            "name": "Alcaraz", "points": 0, "current_set_games": 0, 
            "sets": [], "tiebreak": False, "tiebreak_points": 0, 
            "advantage": False, "winner": False
        },
        "Sinner": {
            "name": "Sinner", "points": 0, "current_set_games": 0, 
            "sets": [], "tiebreak": False, "tiebreak_points": 0, 
            "advantage": False, "winner": False
        }
    })
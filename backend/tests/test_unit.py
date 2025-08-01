import pytest
from main import get_opponent, players_data

def test_get_opponent_returns_correct_player():
    """Unit test: get_opponent should return the other player's name"""
    
    # Test: When given "Alcaraz", should return "Sinner"
    opponent = get_opponent("Alcaraz")
    assert opponent == "Sinner"
    
    # Test: When given "Sinner", should return "Alcaraz"  
    opponent = get_opponent("Sinner")
    assert opponent == "Alcaraz"

def test_get_opponent_with_modified_players_data():
    """Unit test: get_opponent should work with different player data"""
    
    # Temporarily modify players_data for this test
    original_data = players_data.copy()
    
    try:
        # Add a third player temporarily
        players_data["Federer"] = {"name": "Federer"}
        
        # Should still work with original players
        assert get_opponent("Alcaraz") == "Sinner"
        assert get_opponent("Sinner") == "Alcaraz"
        
        # But now Alcaraz could get Federer (first non-Alcaraz player found)
        opponent = get_opponent("Alcaraz")
        assert opponent in ["Sinner", "Federer"]
        
    finally:
        # Restore original data
        players_data.clear()
        players_data.update(original_data)
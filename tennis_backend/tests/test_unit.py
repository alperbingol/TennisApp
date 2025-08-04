"""
Updated unit tests for helper functions.
Tests individual utility functions in isolation.
"""

import pytest
from tennis_backend.tennis_game import get_opponent_from_players


def test_get_opponent_from_players():
    """Unit test: get_opponent_from_players should return the other player's name"""
    
    # Create test players data
    test_players = {
        "Alcaraz": {"name": "Alcaraz"},
        "Sinner": {"name": "Sinner"}
    }
    
    # Test: When given "Alcaraz", should return "Sinner"
    opponent = get_opponent_from_players(test_players, "Alcaraz")
    assert opponent == "Sinner"
    
    # Test: When given "Sinner", should return "Alcaraz"  
    opponent = get_opponent_from_players(test_players, "Sinner")
    assert opponent == "Alcaraz"


def test_get_opponent_with_multiple_players():
    """Unit test: get_opponent_from_players should work with more than 2 players"""
    
    # Create test data with 3 players
    test_players = {
        "Alcaraz": {"name": "Alcaraz"},
        "Sinner": {"name": "Sinner"},
        "Federer": {"name": "Federer"}
    }
    
    # Should return first non-current player found
    opponent = get_opponent_from_players(test_players, "Alcaraz")
    assert opponent in ["Sinner", "Federer"]
    assert opponent != "Alcaraz"


def test_get_opponent_edge_cases():
    """Unit test: Test edge cases for get_opponent_from_players"""
    
    # Test with minimal data
    test_players = {
        "Player1": {"name": "Player1"},
        "Player2": {"name": "Player2"}
    }
    
    opponent = get_opponent_from_players(test_players, "Player1")
    assert opponent == "Player2"
    
    opponent = get_opponent_from_players(test_players, "Player2")  
    assert opponent == "Player1"
"""
Pure unit tests for tennis game logic.
These test the business rules directly without any HTTP/web dependencies.
They're fast, focused, and easy to understand.
"""

import sys
import os

# Add the backend directory to sys.path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tennis_game import award_point_to_player, check_match_win, check_set_win, check_tiebreak_win


def create_fresh_player(name="Player"):
    """Helper to create a fresh player state"""
    return {
        "name": name,
        "points": 0,
        "current_set_games": 0,
        "sets": [],
        "tiebreak": False,
        "tiebreak_points": 0,
        "advantage": False,
        "winner": False
    }


def test_basic_score_progression():
    """Test the basic tennis scoring: 0 → 15 → 30 → 40"""
    player = create_fresh_player("Alcaraz")
    opponent = create_fresh_player("Sinner")
    
    # Award 3 points and verify progression
    player, opponent = award_point_to_player(player, opponent)
    assert player["points"] == 15, "First point should be 15"
    
    player, opponent = award_point_to_player(player, opponent)
    assert player["points"] == 30, "Second point should be 30"
    
    player, opponent = award_point_to_player(player, opponent)
    assert player["points"] == 40, "Third point should be 40"


def test_win_game_from_40():
    """Test winning a game: 40 → win (points reset to 0, games increase by 1)"""
    player = create_fresh_player("Alcaraz")
    opponent = create_fresh_player("Sinner")
    
    # Get player to 40 points
    player["points"] = 40
    
    # Win the game
    player, opponent = award_point_to_player(player, opponent)
    
    assert player["points"] == 0, "Points should reset after winning game"
    assert player["current_set_games"] == 1, "Games should increase by 1"


def test_deuce_scenario():
    """Test deuce: when both players reach 40, next point gives advantage"""
    player = create_fresh_player("Alcaraz")
    opponent = create_fresh_player("Sinner")
    
    # Set up deuce (both at 40)
    player["points"] = 40
    opponent["points"] = 40
    
    # Player wins next point → should get advantage
    player, opponent = award_point_to_player(player, opponent)
    
    assert player["advantage"] == True, "Player should have advantage"
    assert opponent["advantage"] == False, "Opponent should not have advantage"
    assert player["points"] == 40, "Points should stay at 40 during deuce"
    assert opponent["points"] == 40, "Opponent points should stay at 40 during deuce"


def test_advantage_to_win_game():
    """Test: Advantage + win point = win the game"""
    player = create_fresh_player("Alcaraz")
    opponent = create_fresh_player("Sinner")
    
    # Set up advantage situation
    player["points"] = 40
    opponent["points"] = 40
    player["advantage"] = True
    
    # Player wins the next point → should win the game
    player, opponent = award_point_to_player(player, opponent)
    
    assert player["points"] == 0, "Points should reset"
    assert player["current_set_games"] == 1, "Should win the game"
    assert player["advantage"] == False, "Advantage should be cleared"


def test_advantage_back_to_deuce():
    """Test: Player has advantage, opponent wins point → back to deuce"""
    player = create_fresh_player("Alcaraz")
    opponent = create_fresh_player("Sinner")
    
    # Set up: Player has advantage
    player["points"] = 40
    opponent["points"] = 40
    player["advantage"] = True
    
    # Opponent wins the next point → should remove advantage
    opponent, player = award_point_to_player(opponent, player)
    
    assert player["advantage"] == False, "Advantage should be removed"
    assert opponent["advantage"] == False, "Opponent should not get advantage"
    assert player["points"] == 40, "Both should stay at 40"
    assert opponent["points"] == 40, "Both should stay at 40"


def test_set_win_6_0():
    """Test winning a set 6-0"""
    player = create_fresh_player("Alcaraz")
    opponent = create_fresh_player("Sinner")
    
    # Set player to 5 games, then win the 6th
    player["current_set_games"] = 5
    opponent["current_set_games"] = 0
    player["points"] = 40  # Ready to win
    
    # Win the game (and set)
    player, opponent = award_point_to_player(player, opponent)
    
    # Should win the set
    assert len(player["sets"]) == 1, "Should have completed 1 set"
    assert player["sets"][0] == 6, "Should have won 6 games"
    assert opponent["sets"][0] == 0, "Opponent should have 0 games"
    
    # Should reset for next set
    assert player["current_set_games"] == 0, "Games should reset"
    assert opponent["current_set_games"] == 0, "Games should reset"


def test_tiebreak_triggered_at_6_6():
    """Test that tiebreak is triggered when both players reach 6 games"""
    player = create_fresh_player("Alcaraz")
    opponent = create_fresh_player("Sinner")
    
    # Set both to 6 games
    player["current_set_games"] = 6
    opponent["current_set_games"] = 6
    
    # Next point should trigger tiebreak
    player, opponent = award_point_to_player(player, opponent)
    
    assert player["tiebreak"] == True, "Both should be in tiebreak"
    assert opponent["tiebreak"] == True, "Both should be in tiebreak"
    assert player["tiebreak_points"] == 1, "Player should have 1 tiebreak point"
    assert opponent["tiebreak_points"] == 0, "Opponent should have 0 tiebreak points"
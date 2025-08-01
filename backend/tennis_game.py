from typing import Dict, List, Tuple

# Tennis scoring system constants
POINTS_SEQUENCE = [0, 15, 30, 40]

def get_opponent_from_players(players_data: Dict, current_player_name: str) -> str:
    """Get the opponent's name from the players data"""
    return [name for name in players_data if name != current_player_name][0]

def check_match_win(player: Dict, opponent: Dict) -> bool:
    """Check if player has won the match (first to win 3 sets)"""
    if not player["sets"] or not opponent["sets"]:
        return False
    
    player_sets_won = sum(1 for set1, set2 in zip(player["sets"], opponent["sets"]) if set1 > set2)
    if player_sets_won >= 3:
        player["winner"] = True
        opponent["winner"] = False
        return True
    return False

def check_set_win(player: Dict, opponent: Dict) -> bool:
    """Check if player has won the current set"""
    # Normal set win (not tiebreak)
    if player["current_set_games"] >= 6 and (player["current_set_games"] - opponent["current_set_games"]) >= 2:
        player["sets"].append(player["current_set_games"])
        opponent["sets"].append(opponent["current_set_games"])
        _reset_for_new_set(player, opponent)
        check_match_win(player, opponent)
        return True
    return False

def check_tiebreak_win(player: Dict, opponent: Dict) -> bool:
    """Check if player has won the tiebreak"""
    if player["tiebreak_points"] >= 7 and (player["tiebreak_points"] - opponent["tiebreak_points"]) >= 2:
        player["sets"].append(player["current_set_games"] + 1)  # 7 games (6 + tiebreak win)
        opponent["sets"].append(opponent["current_set_games"])   # 6 games
        _reset_for_new_set(player, opponent)
        check_match_win(player, opponent)
        return True
    return False

def _reset_for_new_set(player: Dict, opponent: Dict) -> None:
    """Helper function to reset both players for a new set"""
    for p in [player, opponent]:
        p["current_set_games"] = 0
        p["points"] = 0
        p["advantage"] = False
        p["tiebreak"] = False
        p["tiebreak_points"] = 0

def award_point_to_player(player: Dict, opponent: Dict) -> Tuple[Dict, Dict]:
    """
    Award a point to the player according to tennis rules.
    
    This function contains all the core tennis logic:
    - Normal point progression (0 → 15 → 30 → 40)
    - Deuce and advantage handling
    - Game winning
    - Set winning  
    - Tiebreak logic
    - Match winning
    
    Args:
        player: The player who won the point
        opponent: The other player
        
    Returns:
        Tuple of (updated_player, updated_opponent)
    """
    
    # Tiebreak logic
    if player["tiebreak"]:
        player["tiebreak_points"] += 1
        check_tiebreak_win(player, opponent)
        return player, opponent

    # Enter tiebreak if both reach 6 games in current set
    if player["current_set_games"] == 6 and opponent["current_set_games"] == 6:
        player["tiebreak"] = True
        opponent["tiebreak"] = True
        player["tiebreak_points"] = 1
        opponent["tiebreak_points"] = 0
        return player, opponent

    # Both players at 40: next point is Advantage
    if player["points"] == 40 and opponent["points"] == 40:
        if not player["advantage"] and not opponent["advantage"]:
            player["advantage"] = True
        elif player["advantage"]:
            # Player wins the game
            _win_game(player, opponent)
        elif opponent["advantage"]:
            # Remove opponent's advantage (back to deuce)
            opponent["advantage"] = False
    # Player has 40, opponent less than 40: win game
    elif player["points"] == 40 and opponent["points"] < 40:
        _win_game(player, opponent)
    # Player has Advantage, wins point: win game
    elif player["advantage"]:
        _win_game(player, opponent)
    else:
        # Normal point increment
        if player["points"] in POINTS_SEQUENCE:
            idx = POINTS_SEQUENCE.index(player["points"])
            if idx < len(POINTS_SEQUENCE) - 1:
                player["points"] = POINTS_SEQUENCE[idx + 1]
    
    return player, opponent

def _win_game(player: Dict, opponent: Dict) -> None:
    """Helper function to handle winning a game"""
    player["current_set_games"] += 1
    player["points"] = 0
    opponent["points"] = 0
    player["advantage"] = False
    opponent["advantage"] = False
    check_set_win(player, opponent)
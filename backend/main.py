from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List
import json
import os

app = FastAPI(title="Tennis App API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tennis scoring system
POINTS_SEQUENCE = [0, 15, 30, 40]

# Data model
class PlayerScore(BaseModel):
    name: str
    points: int
    current_set_games: int
    sets: List[int]
    tiebreak: bool = False
    tiebreak_points: int = 0
    advantage: bool = False

# In-memory storage (in a real app, you'd use a database)
players_data = {
    "Alcaraz": {"name": "Alcaraz", "points": 0, "current_set_games": 0, "sets": [], "tiebreak": False, "tiebreak_points": 0, "advantage": False, "winner": False},
    "Sinner": {"name": "Sinner", "points": 0, "current_set_games": 0, "sets": [], "tiebreak": False, "tiebreak_points": 0, "advantage": False, "winner": False}
}

def get_opponent(player_name: str):
    return [p for p in players_data if p != player_name][0]

def check_match_win(player, opponent):
    count = sum(1 for set1, set2 in zip(player["sets"],opponent["sets"]) if set1 > set2)
    if count == 3:
        player["winner"] = True
        opponent["winner"] = False
        return True
    return False

def check_set_win(player, opponent):
    # Normal set win (not tiebreak)
    if player["current_set_games"] >= 6 and (player["current_set_games"] - opponent["current_set_games"]) >= 2:
        player["sets"].append(player["current_set_games"])
        opponent["sets"].append(opponent["current_set_games"])
        player["current_set_games"] = 0
        opponent["current_set_games"] = 0
        player["points"] = 0
        opponent["points"] = 0
        player["advantage"] = False
        opponent["advantage"] = False
        player["tiebreak"] = False
        opponent["tiebreak"] = False
        player["tiebreak_points"] = 0
        opponent["tiebreak_points"] = 0
        check_match_win(player, opponent)
        return True
    return False

def check_tiebreak_win(player, opponent):
    if player["tiebreak_points"] >= 7 and (player["tiebreak_points"] - opponent["tiebreak_points"]) >= 2:
        player["sets"].append(player["current_set_games"] + 1)
        opponent["sets"].append(opponent["current_set_games"] )
        player["current_set_games"] = 0
        opponent["current_set_games"] = 0
        player["points"] = 0
        opponent["points"] = 0
        player["advantage"] = False
        opponent["advantage"] = False
        player["tiebreak"] = False
        opponent["tiebreak"] = False
        player["tiebreak_points"] = 0
        opponent["tiebreak_points"] = 0
        check_match_win(player, opponent)
        return True
    return False

@app.get("/")
async def root():
    return {"message": "Tennis App API is running!"}

@app.get("/players")
async def get_players():
    """Get all players and their scores"""
    return list(players_data.values())

# Not used currently
@app.get("/players/{player_name}")
async def get_player(player_name: str):
    """Get a specific player's score"""
    if player_name not in players_data:
        raise HTTPException(status_code=404, detail="Player not found")
    return players_data[player_name]

@app.post("/players/{player_name}/increment")
async def increment_score(player_name: str):
    """Increment a player's point according to tennis rules, sets, and tiebreaks"""
    if player_name not in players_data:
        raise HTTPException(status_code=404, detail="Player not found")
    opponent_name = get_opponent(player_name)
    player = players_data[player_name]
    opponent = players_data[opponent_name]

    # Tiebreak logic
    if player["tiebreak"]:
        player["tiebreak_points"] += 1
        if check_tiebreak_win(player, opponent):
            return player
        return player

    # Enter tiebreak if both reach 6 games in current set
    if player["current_set_games"] == 6 and opponent["current_set_games"] == 6:
        player["tiebreak"] = True
        opponent["tiebreak"] = True
        player["tiebreak_points"] = 0
        opponent["tiebreak_points"] = 0
        return player

    # Both players at 40: next point is Advantage
    if player["points"] == 40 and opponent["points"] == 40:
        if not player["advantage"] and not opponent["advantage"]:
            player["advantage"] = True
        elif player["advantage"]:
            # Player wins the game
            player["current_set_games"] += 1
            player["points"] = 0
            opponent["points"] = 0
            player["advantage"] = False
            opponent["advantage"] = False
            if check_set_win(player, opponent):
                return player
        elif opponent["advantage"]:
            # Remove opponent's advantage
            opponent["advantage"] = False
    # Player has 40, opponent less than 40: win game
    elif player["points"] == 40 and opponent["points"] < 40:
        player["current_set_games"] += 1
        player["points"] = 0
        opponent["points"] = 0
        player["advantage"] = False
        opponent["advantage"] = False
        if check_set_win(player, opponent):
            return player
    # Player has Advantage, wins point: win game
    elif player["advantage"]:
        player["current_set_games"] += 1
        player["points"] = 0
        opponent["points"] = 0
        player["advantage"] = False
        opponent["advantage"] = False
        if check_set_win(player, opponent):
            return player
    else:
        # Normal point increment
        if player["points"] in POINTS_SEQUENCE:
            idx = POINTS_SEQUENCE.index(player["points"])
            if idx < len(POINTS_SEQUENCE) - 1:
                player["points"] = POINTS_SEQUENCE[idx + 1]
    return player

@app.post("/players/reset")
async def reset_scores():
    """Reset all player points, games, sets, and tiebreaks to 0"""
    for player in players_data.values():
        player["points"] = 0
        player["current_set_games"] = 0
        player["sets"] = []
        player["tiebreak"] = False
        player["tiebreak_points"] = 0
        player["advantage"] = False
        player["winner"] = False
    return list(players_data.values())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
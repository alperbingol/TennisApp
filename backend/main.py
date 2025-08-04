from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List
import json
import os
import sys
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from tennis_game import award_point_to_player, get_opponent_from_players

app = FastAPI(title="Tennis App API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# POINTS_SEQUENCE moved to tennis_game.py

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

# Tennis logic functions moved to tennis_game.py

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
    # Web layer: Handle HTTP-specific concerns
    if player_name not in players_data:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Get player data
    opponent_name = get_opponent_from_players(players_data, player_name)
    player = players_data[player_name]
    opponent = players_data[opponent_name]
    
    # Business layer: Apply tennis logic (this is where the magic happens!)
    updated_player, updated_opponent = award_point_to_player(player, opponent)
    
    # Update the data store (in a real app, this would be database operations)
    players_data[player_name] = updated_player
    players_data[opponent_name] = updated_opponent
    
    return updated_player

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
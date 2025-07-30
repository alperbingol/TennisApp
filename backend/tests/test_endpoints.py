from fastapi import responses
from fastapi.testclient import TestClient
from main import app

# Create a test client
client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns the correct message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tennis App API is running!"}

def test_get_players():
    """Test that we can get all players """
    response = client.get("/players")
    assert response.status_code == 200 
    data = response.json()
    assert len(data) == 2 

    player_names = [player["name"] for player in data]
    assert "Alcaraz" in player_names
    assert "Sinner" in player_names

def test_get_nonexistent_player():
    """Test what happens when we request a player that doesn't exist"""
    response = client.get("/players/Federer")  # Federer is not in our data
    
    print(f"Status code for nonexistent player: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 404  # Should be "Not Found"
    assert "Player not found" in response.json()["detail"]

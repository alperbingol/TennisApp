import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_BASE_URL = 'http://localhost:8000';

  const winner = players.find(player => player.winner);

  // Fetch players data on component mount
  useEffect(() => {
    fetchPlayers();
  }, []);

  const fetchPlayers = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/players`);
      setPlayers(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch players data. Make sure the backend is running.');
      console.error('Error fetching players:', err);
    } finally {
      setLoading(false);
    }
  };

  const incrementScore = async (playerName) => {
    if (winner) {
      setError('Match already has a winner! Please reset to start a new match.');
      return;
    }
    try {
      await axios.post(`${API_BASE_URL}/players/${playerName}/increment`);
      // Fetch the full updated player list after increment
      const response = await axios.get(`${API_BASE_URL}/players`);
      setPlayers(response.data);
    } catch (err) {
      setError(`Failed to increment score for ${playerName}`);
      console.error('Error incrementing score:', err);
    }
  };

  const resetScores = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/players/reset`);
      setPlayers(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to reset scores');
      console.error('Error resetting scores:', err);
    }
  };

  if (loading) {
    return (
      <div className="tennis-app">
        <h1 className="app-title">🎾 Tennis App</h1>
        <p className="loading">Loading players...</p>
      </div>
    );
  }

 

  return (
    <div className="tennis-app">
      <h1 className="app-title">🎾 Tennis App</h1>
      
      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {winner && <div>Winner: {winner.name}</div>}

      <div className="scoreboard-header">
        <span className="header-name"></span>
        {/* Render set headers dynamically */}
        {Array.from({ length: Math.max(...players.map(p => p.sets.length)) || 1 }).map((_, idx) => (
          <span key={idx} className="header-set">Set {idx + 1}</span>
        ))}
        <span className="header-games">Games</span>
        <span className="header-points">Points</span>
        <span className="header-action"></span>
      </div>

      <div className="players-container">
        {players.map((player) => (
          <div key={player.name} className="player-card">
            <div className="player-info">
              <span className="player-name">{player.name}</span>
              {/* Render finished sets */}
              {Array.from({ length: Math.max(...players.map(p => p.sets.length)) || 1 }).map((_, idx) => (
                <span key={idx} className="player-set-square">
                  {player.sets[idx] !== undefined ? player.sets[idx] : ''}
                </span>
              ))}
              <span className="player-games-square">{player.current_set_games}</span>
              <span 
                className="player-score"
                onClick={() => incrementScore(player.name)}
                style={{ cursor: 'pointer' }}
                title="Click to add a point"
              >
                {player.tiebreak
                  ? player.tiebreak_points
                  : player.advantage
                    ? 'Ad'
                    : (players.some(p => p.advantage) ? '' : player.points)
                }
              </span>
            </div>
          </div>
        ))}
      </div>

       
  

      <button 
        className="reset-btn"
        onClick={resetScores}
      >
        Reset All Scores
      </button>

 
    </div>
  );
}

export default App; 
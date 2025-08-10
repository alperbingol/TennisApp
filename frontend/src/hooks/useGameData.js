import { useState, useEffect, useCallback } from 'react';
import { fetchPlayers, incrementPlayerScore, resetGameScores } from '../services/gameService';

function useGameData() {
  // All the state that was in App.js
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch players using service
  const fetchPlayersData = useCallback(async () => {
    try {
      setLoading(true);
      const playersData = await fetchPlayers();
      setPlayers(playersData);
      setError(null);
    } catch (err) {
      setError('Failed to fetch players data. Make sure the backend is running.');
      console.error('Error fetching players:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const incrementScore = useCallback(async (playerName) => {
    const winner = players.find(player => player.winner);
    if (winner) {
      setError('Match already has a winner! Please reset to start a new match.');
      return;
    }
    try {
      const updatedPlayers = await incrementPlayerScore(playerName);
      setPlayers(updatedPlayers);
    } catch (err) {
      setError(`Failed to increment score for ${playerName}`);
      console.error('Error incrementing score:', err);
    }
  }, [players]);

  const resetScores = useCallback(async () => {
    try {
      const resetPlayers = await resetGameScores();
      setPlayers(resetPlayers);
      setError(null);
    } catch (err) {
      setError('Failed to reset scores');
      console.error('Error resetting scores:', err);
    }
  }, []);

  // The effect that was in App.js
  useEffect(() => {
    fetchPlayersData();
  }, [fetchPlayersData]);

  // Return everything the component needs
  return {
    players,
    loading,
    error,
    incrementScore,
    resetScores
  };
}

export default useGameData;
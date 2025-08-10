import axios from 'axios';

// Get the API base URL (same logic as before, but centralized)
const getApiBaseUrl = () => {
  return process.env.REACT_APP_API_URL || 'http://localhost:8000';
};

// Pure API functions - no React hooks, no state management
export const fetchPlayers = async () => {
  const response = await axios.get(`${getApiBaseUrl()}/players`);
  return response.data;
};

export const incrementPlayerScore = async (playerName) => {
  await axios.post(`${getApiBaseUrl()}/players/${playerName}/increment`);
  // After incrementing, fetch fresh data
  const response = await axios.get(`${getApiBaseUrl()}/players`);
  return response.data;
};

export const resetGameScores = async () => {
  const response = await axios.post(`${getApiBaseUrl()}/players/reset`);
  return response.data;
};
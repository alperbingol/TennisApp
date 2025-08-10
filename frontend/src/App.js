import React from 'react';
import './App.css';
import Loading from './components/common/Loading';
import ErrorMessage from './components/common/ErrorMessage';
import WinnerBanner from './components/game/WinnerBanner';
import PlayerCard from './components/game/PlayerCard';
import ScoreboardHeader from './components/game/ScoreboardHeader';
import Button from './components/common/Button';
import useGameData from './hooks/useGameData';


function App() {
  // All business logic now comes from our custom hook!
  const { players, loading, error, incrementScore, resetScores } = useGameData();
  const winner = players.find(player => player.winner);

  if (loading) {
    return <Loading />;
  }

  return (
    <div className="tennis-app">
      <h1 className="app-title">🎾 Tennis App</h1>
      
      <ErrorMessage message={error}/>

      <WinnerBanner winner={winner} />

      <ScoreboardHeader maxSets={Math.max(...players.map(p => p.sets.length)) || 1} />

      <div className="players-container">
        {players.map((player) => (
          <PlayerCard 
            key={player.name}
            player={player}
            maxSets={Math.max(...players.map(p => p.sets.length)) || 1}
            onScoreIncrement={incrementScore}
            players={players}
          />
        ))}
      </div>

      <Button 
        className="reset-btn"
        onClick={resetScores}
      >
        Reset All Scores
      </Button>

 
    </div>
  );
}

export default App; 
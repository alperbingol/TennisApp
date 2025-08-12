import React from 'react';
import '../../App.css';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';
import WinnerBanner from './WinnerBanner';
import PlayerCard from './PlayerCard';
import ScoreboardHeader from './ScoreboardHeader';
import Button from '../common/Button';
import useGameData from '../../hooks/useGameData';


function Game() {
  // All business logic now comes from our custom hook!
  const { players, loading, error, incrementScore, resetScores } = useGameData();
  const winner = players.find(player => player.winner);

  if (loading) {
    return <Loading />;
  }

  if (error){

    return (<div className="tennis-app">
    <ErrorMessage message={error}/>
    </div>
    )
  }

  return (
    <div className="tennis-app">
      <h1 className="app-title">🎾 Tennis App</h1>
      
      

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

export default Game; 
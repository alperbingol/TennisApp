import React from 'react';
import '../../App.css';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';
import WinnerBanner from './WinnerBanner';
import PlayerCard from './PlayerCard';
import ScoreboardHeader from './ScoreboardHeader';
import Button from '../common/Button';
import useGameData from '../../hooks/useGameData';
import { useLocation, useNavigate } from 'react-router-dom';


function Game() {
  // All business logic now comes from our custom hook!
  const { players, loading, error, incrementScore, resetScores } = useGameData();
  const winner = players.find(player => player.winner);

  const nav = useNavigate();

  const {state} = useLocation();
  const customNames = [
    state?.player1.trim(),
    state?.player2.trim()
  ];


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
        {players.map((player, idx) => (
          <PlayerCard 
            key={player.name}
            player={player}
            maxSets={Math.max(...players.map(p => p.sets.length)) || 1}
            onScoreIncrement={incrementScore}
            players={players}
            displayName={customNames[idx] || player.name}
          />
        ))}
      </div>

      <Button 
        className="reset-btn"
        onClick={resetScores}
      >
        Reset All Scores
      </Button>

      <Button onClick={()=>nav('/', {replace:true})}> Home </Button>
    </div>
  );
}

export default Game; 
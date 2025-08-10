function PlayerCard({ player, maxSets, onScoreIncrement, players }) {
  const displayPoints = () => {
    if (player.tiebreak) {
      return player.tiebreak_points;
    }
    if (player.advantage) {
      return 'Ad';
    }
    if (players.some(p => p.advantage)) {
      return '';
    }
    return player.points;
  };

  return (
    <div className="player-card">
      <div className="player-info">
        <span className="player-name">{player.name}</span>
        
        {/* Render finished sets */}
        {Array.from({ length: maxSets || 1 }).map((_, idx) => (
          <span key={idx} className="player-set-square">
            {player.sets[idx] !== undefined ? player.sets[idx] : ''}
          </span>
        ))}
        
        <span className="player-games-square">{player.current_set_games}</span>
        
        <span 
          className="player-score"
          onClick={() => onScoreIncrement(player.name)}
          style={{ cursor: 'pointer' }}
          title="Click to add a point"
        >
          {displayPoints()}
        </span>
      </div>
    </div>
  );
}

export default PlayerCard;
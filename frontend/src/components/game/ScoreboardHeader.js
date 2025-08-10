function ScoreboardHeader({ maxSets }) {
  return (
    <div className="scoreboard-header">
      <span className="header-name"></span>
      
      {/* Render set headers dynamically */}
      {Array.from({ length: maxSets || 1 }).map((_, idx) => (
        <span key={idx} className="header-set">Set {idx + 1}</span>
      ))}
      
      <span className="header-games">Games</span>
      <span className="header-points">Points</span>
    </div>
  );
}

export default ScoreboardHeader;
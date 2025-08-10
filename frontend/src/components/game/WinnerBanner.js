function WinnerBanner({ winner }) {
  if (!winner) return null;
  
  return (
    <div className="winner-banner">
      Winner: {winner.name}
    </div>
  );
}

export default WinnerBanner;
function Loading({ message = "Loading players..." }) {
  return (
    <div className="tennis-app">
      <h1 className="app-title">🎾 Tennis App</h1>
      <p className="loading">{message}</p>
    </div>
  );
}

export default Loading;
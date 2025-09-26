import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomepageUserLogin from './components/start/start';
import MainScoreBoard from './components/game/Game';


function App() {

  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<HomepageUserLogin />} />
          <Route path="/game" element={<MainScoreBoard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 
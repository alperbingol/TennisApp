import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Game from './components/game/Game';
import Hello from './components/start/start';


function App() {

  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Hello />} />
          <Route path="/game" element={<Game />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 
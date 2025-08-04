# 🎾 Tennis App

A professional tennis scoring API built with FastAPI and modern Python packaging. Features comprehensive tennis game logic including regular scoring, deuce/advantage, sets, tiebreaks, and match completion with a React frontend for real-time score tracking.

## Features

### 🎾 Tennis Logic
- **Complete Tennis Rules**: Accurate scoring (0-15-30-40), deuce/advantage, games, sets
- **Tiebreak Support**: Automatic tiebreak at 6-6 with proper tiebreak scoring  
- **Match Completion**: Best-of-5 sets with winner detection
- **Professional API**: Clean FastAPI endpoints for all tennis operations

### 🌐 Web Interface  
- **Real-time Score Tracking**: Click buttons to increment scores for each player
- **Modern UI**: Beautiful gradient design with smooth animations
- **Reset Functionality**: Reset all scores to zero with one click
- **Responsive Design**: Works on desktop and mobile devices (future plan)

### 🧪 Testing & Quality
- **Comprehensive Test Suite**: Unit tests, API tests, and integration tests
- **Professional Structure**: Installable Python package with clean imports
- **Development Ready**: Hot reload, linting, and modern development workflow

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.8+**: Professional package structure with pyproject.toml
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI

### Frontend  
- **React**: JavaScript library for building user interfaces
- **Axios**: HTTP client for API communication
- **CSS3**: Modern styling with gradients and animations

### Development & Testing
- **pytest**: Comprehensive test suite with unit, API, and integration tests
- **Modern Packaging**: pip-installable package with clean dependency management
- **Professional Structure**: Separation of concerns with clean imports

## Project Structure

```
TennisApp/
├── pyproject.toml              # Modern Python package configuration
├── tennis_backend/             # Main Python package  
│   ├── __init__.py            # Package marker
│   ├── main.py                # FastAPI application
│   ├── tennis_game.py         # Core tennis logic (pure Python)
│   ├── TESTING_GUIDE.md       # Comprehensive testing documentation
│   └── tests/                 # Test suite
│       ├── test_tennis_unit.py     # Unit tests (tennis logic)
│       ├── test_endpoints.py       # API contract tests  
│       ├── test_tennis_integration.py # Full workflow tests
│       └── conftest.py            # pytest configuration
├── frontend/                   # React application
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   ├── App.css            # Styling
│   │   └── index.js           # React entry point
│   └── package.json           # Frontend dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** 
- **Node.js 14+** 
- **Git** (to clone the repository)

### 🏃‍♂️ One-Time Setup

**1. Clone and enter the project:**
```bash
git clone <your-repo-url>
cd TennisApp
```

**2. Set up Python backend (one command!):**
```bash
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate              # Windows
# source .venv/bin/activate           # macOS/Linux

# Install the tennis backend package with all dependencies
pip install -e .[dev]
```

**3. Set up React frontend:**
```bash
cd frontend
npm install
cd ..
```

### ⚡ Daily Usage (After Setup)

**Start the backend:**
```bash
# Activate environment (if not already active)
.\.venv\Scripts\activate

# Start the API server (works from any directory!)
uvicorn tennis_backend.main:app --reload
```
**Backend runs at:** `http://localhost:8000`

**Start the frontend (new terminal):**
```bash
cd frontend
npm start
```
**Frontend runs at:** `http://localhost:3000`

## 🧪 Testing

**Run the comprehensive test suite:**

```bash
# Activate environment
.\.venv\Scripts\activate

# Run all tests
pytest tennis_backend/tests/ -v

# Run specific test types
pytest tennis_backend/tests/test_tennis_unit.py -v      # Unit tests (fastest)
pytest tennis_backend/tests/test_endpoints.py -v       # API tests  
pytest tennis_backend/tests/test_tennis_integration.py -v # Integration tests
```

## 🔧 Development

**The package structure supports professional development:**

```bash
# Your package is installed in editable mode, so changes are immediate
# Edit any file in tennis_backend/ and changes are reflected instantly

# Import your tennis logic anywhere:
python -c "from tennis_backend.tennis_game import award_point_to_player"

# Run the server from any directory:
uvicorn tennis_backend.main:app --reload

# Clean, professional imports throughout:
from tennis_backend.main import app
from tennis_backend.tennis_game import award_point_to_player
```

## API Endpoints

The FastAPI backend provides the following endpoints:

- `GET /` - Health check
- `GET /players` - Get all players and their scores
- `GET /players/{player_name}` - Get a specific player's score
- `POST /players/{player_name}/increment` - Increment a player's score
- `POST /players/reset` - Reset all player scores to 0

## 🎮 Usage

1. **Start both servers** (backend and frontend)
2. **Open your browser** and go to `http://localhost:3000`
3. **Play tennis**: Click point buttons to increment scores for Alcaraz and Sinner
4. **Watch the magic**: Automatic deuce/advantage handling, set progression, tiebreaks
5. **Reset anytime**: Use the reset button to start a new match

**API Documentation**: Visit `http://localhost:8000/docs` for interactive API docs



## 📄 License

This project is open source and available under the MIT License.
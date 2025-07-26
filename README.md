# 🎾 Tennis App

A full-stack tennis score tracking application built with FastAPI (backend) and React (frontend). Track scores for tennis players Alcaraz and Sinner with a beautiful, modern UI.

## Features

- **Real-time Score Tracking**: Click buttons to increment scores for each player
- **Modern UI**: Beautiful gradient design with smooth animations
- **Reset Functionality**: Reset all scores to zero with one click
- **Responsive Design**: Works on desktop, mobile devices in future
- **Error Handling**: Graceful error handling with user-friendly messages

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **React**: JavaScript library for building user interfaces
- **Axios**: HTTP client for API communication
- **CSS3**: Modern styling with gradients and animations

## Project Structure

```
TennisApp/
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html       # Main HTML file
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # App-specific styles
│   │   ├── index.js         # React entry point
│   │   └── index.css        # Global styles
│   └── package.json         # Node.js dependencies
└── README.md               # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8+ installed
- Node.js 14+ installed
- npm or yarn package manager

### Manual Setup

#### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
     ```
     .\.venv\Scripts\activate
     ```
     ```
     source venv/Scripts/activate
     ```

4. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the FastAPI server:
   ```
   python main.py
   ```
   ```
   uvicorn backend.main:app --reload
   ```
   The backend will be available at `http://localhost:8000`

#### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`

## API Endpoints

The FastAPI backend provides the following endpoints:

- `GET /` - Health check
- `GET /players` - Get all players and their scores
- `GET /players/{player_name}` - Get a specific player's score
- `POST /players/{player_name}/increment` - Increment a player's score
- `POST /players/reset` - Reset all player scores to 0

## Usage

1. Open your browser and go to `http://localhost:3000`
2. You'll see two player cards: one for Alcaraz and one for Sinner
3. Click the points button next to any player to increment their score
4. Use the "Reset All Scores" button to reset both players' scores to zero

## Development

### Backend Development

- The backend uses in-memory storage for simplicity
- API documentation is available at `http://localhost:8000/docs` when the server is running

### Frontend Development

- The React app uses functional components with hooks
- Axios is used for API communication
- The UI is fully responsive and includes loading states and error handling


## License

This project is open source and available under the MIT License. 
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function HomepageUserLogin(){

    const [players, setPlayers] = useState({ player1: '', player2: ''});
    
    const navigate = useNavigate();

    const handleStartGame = () => {

        if (players.player1.trim() && players.player2.trim()){
            navigate('/game', {
                state: {
                    player1: players.player1.trim(),
                    player2: players.player2.trim()
                },
                replace: true
            });
        } else{
            alert('Please enter both player names!');
        }
    };

    return(
        <div>
            <h1>Welcome to Tennis Game!</h1>
            
            <div>
                <div>
                    <label>Player 1 Name:</label>
                    <input 
                        type="text" 
                        placeholder="Enter Player 1 name"
                        onChange={(e)=> setPlayers( prev =>({ ...prev, player1: e.target.value }))}
                        value={players.player1} />
                </div>
                
                <div>
                    <label>Player 2 Name:</label>
                    <input 
                        type="text" 
                        placeholder="Enter Player 2 name"
                        onChange={(e)=> setPlayers( prev => ({ ...prev, player2: e.target.value }))}
                        value={players.player2} />
                </div>
                
                <button onClick={handleStartGame}>
                    Start Game
                </button>
            </div>
        </div>
    )
}

export default HomepageUserLogin;

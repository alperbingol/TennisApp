import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Hello(){

    const [player1Name, setPlayer1Name] = useState('');
    const [player2Name, setPlayer2Name] = useState('');
    
    const navigate = useNavigate();

    const handleStartGame = () => {

        if (player1Name.trim() && player2Name.trim()){
            navigate('/game', {
                state: {
                    player1: player1Name.trim(),
                    player2: player2Name.trim()
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
                        onChange={(e)=> setPlayer1Name(e.target.value)}
                        value={player1Name} />
                </div>
                
                <div>
                    <label>Player 2 Name:</label>
                    <input 
                        type="text" 
                        placeholder="Enter Player 2 name"
                        onChange={(e)=> setPlayer2Name(e.target.value)}
                        value={player2Name} />
                </div>
                
                <button onClick={handleStartGame}>
                    Start Game
                </button>
            </div>
        </div>
    )
}

export default Hello;

import { useNavigate } from "react-router";

function Hello(){

    const navigate = useNavigate();

    return(
        <div>
            <h1>Welcome to Tennis Game!</h1>
            
            <div>
                <div>
                    <label>Player 1 Name:</label>
                    <input type="text" name="Enter Player 1 name" />
                </div>
                
                <div>
                    <label>Player 2 Name:</label>
                    <input type="text" placeholder="Enter Player 2 name" />
                </div>
                
                <button onClick={() => navigate("/game")}>Start Game

                </button>
            </div>
        </div>
    )
}

export default Hello;

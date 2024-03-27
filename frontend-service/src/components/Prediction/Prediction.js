import "./Prediction.css"
import { useState, useEffect } from "react";


function Prediction() { 

    const [prediction, setPrediction] = useState({
        value: 0.0, 
        currency: "$"
    })

    const [data, setdata] = useState("");

    useEffect(() => {
        const url = "ws://localhost:5000/ws"; 
        const ws = new WebSocket(url); 

        ws.onmessage = (e) => {
            const pred = JSON.parse(e.data); 
            setPrediction({
                value: pred, 
                currency: "$"
            });
        }
        
    }, []);
 

    return (
        <div className="Prediction">
            <h1>
                Predicted value: {prediction.value + " " + prediction.currency}
            </h1>
        </div>
    );
}


export default Prediction;
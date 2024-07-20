import "./PredictionBar.css"
import { useState, useEffect } from "react";


const WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m";
const PV_URL = "/predict/"

function Prediction() { 
    const [realValue, setRealValue] = useState({
        time: "", 
        value: 0.0
    }); 
    const [predValue, setPredValue] = useState({
        time: "", 
        value: 0.0
    });
    const ws = new WebSocket(WS_URL); 

    useEffect(() => {
        ws.onmessage = (event) => {
            const response = JSON.parse(event.data);

            setRealValue({
                time: response.k.t / 1000, 
                value: parseFloat(response.k.o)
            });

            fetch(PV_URL)
                .then(res => res.json())
                .then(data => {
                    setPredValue(data);
                })
                .catch(err => console.log(err));
        }

    }, []);


    return (
        <div className="Prediction">
            <h1>
                Real value: {realValue.value}
            </h1>
            <h1>
                Predicted value: {predValue.value}
            </h1>
        </div>
    );
}


export default Prediction;



import "./Prediction.css"
import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Bar, BarChart, ScatterChart, Scatter } from 'recharts';


function Prediction() { 
    const [realValue, setRealValue] = useState({
        value: 0.0, 
        currency: "BTCUSDT"
    }); 
    const [predValue, setPredValue] = useState({
        value: 0.0, 
        currency: "BTCUSDT" 
    });
    const [time, setTime] = useState(new Date());

    useEffect(() => {
        const interval = setInterval(() => {
            setTime(new Date()); 
            const url = "/predict/"; 
            const response = fetch(url)
                .then(response => response.json())
                .then(data => {console.log(data);setPredValue({
                    value: parseFloat(data).toFixed(2), 
                    currency: "BTCUSDT"
                });}
            );
        }, 1000);
        
        return () => clearInterval(interval); 
    }, []); 

    useEffect(() => {
        const url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1s";
        const ws = new WebSocket(url); 

        ws.onmessage = (event) => {
            const response = JSON.parse(event.data); 
            setRealValue({
                value: parseFloat(response.k.c).toFixed(2),    
                currency: response.k.s
            });
        };
    }, []);

    return (
        <div className="Prediction">
            <h1>
                Real value: {realValue.value + " " + realValue.currency}; 
            </h1>
            <h1>
                Predicted value: {predValue.value + " " + predValue.currency}.
            </h1>
        </div>
    );
}


export default Prediction;



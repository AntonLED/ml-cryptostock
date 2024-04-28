import "./Prediction.css"
import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Bar, BarChart, ScatterChart, Scatter } from 'recharts';

function getTime() {
    var now = new Date();
    return (((now.getMinutes() < 10)
                 ? ("0" + now.getMinutes())
                 : (now.getMinutes())) + ':' +
             ((now.getSeconds() < 10)
                 ? ("0" + now.getSeconds())
                 : (now.getSeconds())));
}

function Prediction() { 

    const [prediction, setPrediction] = useState({
        value: 0.0, 
        currency: "BTCUSDT"
    })

    const [data, setData] = useState([{
        price: null, 
        timestamp: null
    }]); 

    useEffect(() => {
        const url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1s";
        const ws = new WebSocket(url); 

        ws.onmessage = (event) => {
            const response = JSON.parse(event.data); 
            setPrediction({
                value: parseFloat(response.k.c).toFixed(2),    
                currency: response.k.s
            });
            setData(
                data => [...data, {
                    price: parseFloat(response.k.c) - 69835.0, 
                    timestamp: getTime()
                }]
            ); 
        };
        
    }, []);

    return (
        <div className="Prediction">
            <h1>
                Predicted value: {prediction.value + " " + prediction.currency}
            </h1>

            <div>
            <ScatterChart width={1000} height={300} data={data} >
                <YAxis dataKey="price" />
                <XAxis />
                <Scatter dataKey="price" fill="cornflowerblue"/>
            </ScatterChart>
            </div>
        </div>
    );
}


export default Prediction;



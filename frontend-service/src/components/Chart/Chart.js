import "./Chart.css"
import { useState, useEffect, useRef } from "react";
import { createChart } from 'lightweight-charts';


const URL = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=1000"; 
const WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m";


function Chart() {
    const chartContainerRef = useRef();
    const chartProps = {
        width: 800, 
        height: 300,
        timeScale: {
            timeVisible: true, 
            secondsVisible: false
        }
    };
    const ws = new WebSocket(WS_URL); 

    useEffect(() => {
        const chart = createChart(chartContainerRef.current, chartProps);
        
        const achart = chart.addAreaSeries();

        fetch(URL)
            .then(res => res.json())
            .then(data => {
                const cdata = data.map(d => {
                    return {
                        time: d[0] / 1000, 
                        value: parseFloat(d[1]) 
                    }
                });

                achart.setData(cdata); 
            })
            .catch(err => console.log(err));

        ws.onmessage = (event) => {
            const response = JSON.parse(event.data);

            console.log("WS"); 

            achart.update({
                time: response.k.t / 1000, 
                value: parseFloat(response.k.o)
            });
        };

        return () => {
            chart.remove();
        }
    }, []);

    return (
        <div className="Chart" ref={chartContainerRef}/>
    )
}


export default Chart;
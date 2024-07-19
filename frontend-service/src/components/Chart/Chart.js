import "./Chart.css"
import { useState, useEffect, useRef } from "react";
import { createChart } from 'lightweight-charts';



function Chart() {
    const chartContainerRef = useRef();
    const chart = useRef();

    const props = {
        width: 800, 
        height: 300,
        timeScale: {
            timeVisible: true, 
            secondsVisible: false
        }
    };

    const url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=100"; 
    const ws_url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m";
    const ws = new WebSocket(ws_url); 

    useEffect(() => {
        chart.current = createChart(chartContainerRef.current, props);
        
        const candleChart = chart.current.addCandlestickSeries();

        fetch(url)
            .then(res => res.json())
            .then(data => {
                const cdata = data.map(d => {
                    return {
                        time: d[0] / 1000, 
                        open: parseFloat(d[1]), 
                        high: parseFloat(d[2]), 
                        low: parseFloat(d[3]), 
                        close: parseFloat(d[4])
                    }
                });

                candleChart.setData(cdata); 
            })
            .catch(err => console.log(err));

        ws.onmessage = (event) => {
            const response = JSON.parse(event.data);

            console.log("WS"); 

            candleChart.update({
                time: response.k.t / 1000, 
                open: parseFloat(response.k.o), 
                high: parseFloat(response.k.h), 
                low: parseFloat(response.k.l), 
                close: parseFloat(response.k.c)
            });
        };

        return () => {
            chart.current.remove();
        }
        
    }, []);

  

    return (
        <div className="Chart" ref={chartContainerRef}/>
    )
}


export default Chart;
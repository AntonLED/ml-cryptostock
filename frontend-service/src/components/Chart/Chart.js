import "./Chart.css"
import { useState, useEffect, useRef } from "react";
import { createChart } from 'lightweight-charts';


const URL = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=1000"; 
const WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m";
const PV_URL = "/predict/"


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

        const achart = chart.addAreaSeries({   
            topColor: 'rgba(67, 83, 254, 0.7)',
            bottomColor: 'rgba(67, 83, 254, 0.3)',
            lineColor: 'rgba(67, 83, 254, 1)',
            lineWidth: 2, 
        });
        const _achart = chart.addAreaSeries({
            topColor: 'rgba(255, 192, 0, 0.7)',
            bottomColor: 'rgba(255, 192, 0, 0.3)',
            lineColor: 'rgba(255, 192, 0, 1)',
            lineWidth: 2,
        });

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

            achart.update({
                time: response.k.t / 1000, 
                value: parseFloat(response.k.o)
            });

            fetch(PV_URL)
            .then(res => res.json())
            .then(data => {
                _achart.update({
                    time: response.k.t / 1000, 
                    value: data.value
                });
            })
            .catch(err => console.log(err));

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
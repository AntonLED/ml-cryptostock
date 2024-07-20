import React, { useState, useEffect } from "react";
import "./App.css";
import Title from "./components/Title/Title";
import PredictionBar from "./components/Prediction/PredictionBar";
import Chart from "./components/Chart/Chart";

 
function App() {

    return (
        <div className="App">
            <div className="App-header">
                <Title/>    
                <PredictionBar/>
                <Chart/>
            </div>
        </div>
    );
}
 
export default App;
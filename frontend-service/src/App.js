import React, { useState, useEffect } from "react";
import "./App.css";
import Title from "./components/Title/Title";
import Prediction from "./components/Prediction/Prediction";
import Chart from "./components/Chart/Chart";

 
function App() {

    return (
        <div className="App">
            <div className="App-header">
                <Title/>    
                <Prediction/>
                <Chart/>
            </div>
        </div>
    );
}
 
export default App;
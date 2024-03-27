import { useState, useEffect, useRef } from "react"; 
import "./Title.css";
import { FadeInAnimation } from "./animation";


function Title () { 
    const ref = useRef(null); 

    useEffect(() => {
        const animating = new FadeInAnimation(ref.current); 
        animating.start(1000); 
        return () => {
            animating.stop();
        }; 
    }, []); 

    return (
        <h1 className="Title" ref={ref}>
            Welcome to ml-cryptostock!
        </h1>
    );
}


export default Title; 
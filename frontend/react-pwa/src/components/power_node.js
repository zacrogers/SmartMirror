import React, {useState, useEffect} from 'react';
import {Button, Container, Divider} from '@mui/material';
import './myStyles.css';

let labels = ["1", "2", "3", "4"];
let nodeLabel = "NodeLabel";

export const PowerNode = (props) =>{
    const [error, setError] = useState(null);
    const [channelLabels, setChannelLabels] = useState([]);
    const [channelStates, setChannelStates] = useState([]);

    useEffect(() => {
        setChannelLabels(labels);
    }, [])

    const setChannelState = (channel) =>{
        if(channelStates[channel]){
            // Turn off
        }else{
            //Turn on
        }
    }

    return(
        <div className="card-element">
            {/* <Container> */}
            <div className="card-element-heading">
                <label>{props.label}</label>
                <div className="card-element-divider"></div>
            </div>
            {/* <br/> */}
            <div className="power-node-container">
                <Button variant="contained" onClick={()=>{setChannelState(0)}}>1</Button>
                <Button variant="contained" onClick={()=>{setChannelState(1)}}>2</Button>
                <Button variant="contained" onClick={()=>{setChannelState(2)}}>3</Button>
                <Button variant="contained" onClick={()=>{setChannelState(3)}}>4</Button>
            {/* {channelLabels.map(label=>
                    <Button
                        disabled={error ? "true":"false"}
                        variant="contained">
                        {label}
                    </Button>
            )} */}
            </div>
            {/* </Container> */}
        </div>
    )
}

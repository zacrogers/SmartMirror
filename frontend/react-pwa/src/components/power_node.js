import React, {useState, useEffect} from 'react';
import {Button, Container, Divider} from '@mui/material';
import './myStyles.css';

let labels = ["1", "2", "3", "4"];
let nodeLabel = "NodeLabel";

export const PowerNode = (props) =>{
    const [error, setError] = useState(null);
    const [channelLabels, setChannelLabels] = useState([]);

    useEffect(() => {
        setChannelLabels(labels);
    }, [])

    return(
        <div className="card-element">
            {/* <Container> */}
            <div className="card-element-heading">
                <label>{props.label}</label>
                <div className="card-element-divider"></div>
            </div>
            {/* <br/> */}
            <div className="power-node-container">
                <Button variant="contained">1</Button>
                <Button variant="contained">1</Button>
                <Button variant="contained">1</Button>
                <Button variant="contained">1</Button>
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

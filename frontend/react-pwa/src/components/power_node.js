import React, {useState, useEffect} from 'react';
import {Button, Container} from '@mui/material';
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
            <Container>
            <label>{props.label}</label>
            <br/>
            {channelLabels.map(label=>
                    <Button
                        disabled={error ? "true":"false"}
                        variant="contained">
                        {label}
                    </Button>
            )}
            </Container>
        </div>
    )
}

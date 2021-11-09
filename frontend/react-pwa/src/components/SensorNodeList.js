import React, {useState, useEffect} from 'react';
import {Button, Container} from '@mui/material';


export const SensorNodeList = (props) => {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [sensorLabels, setSensorLabels] = useState({});

    useEffect(() => {
        fetch('http://'+props.api_ip+'/node_info?'+new URLSearchParams({'get_all_labels':1}))
            .then(res => res.json())
            .then(
                (data) =>{
                    setIsLoaded(true);
                    setSensorLabels(data);
                },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            )
    }, [])

    if(error){
        return <div>Error: {error.message}</div>
    } else if (!isLoaded){
        return <div> Loading...</div>
    } else {
        return(
            <div >
                <select className="node-form-inputs">
                    {Object.values(sensorLabels).map(label=>
                        <option>
                            {label}
                        </option>
                    )}
                </select>
            </div>
        )
    }
}

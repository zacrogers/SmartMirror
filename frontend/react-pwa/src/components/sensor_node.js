import React, {useState, useEffect} from 'react';
import {Button, Container} from '@mui/material';

export const SensorNodeData = (props) => {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [sensorData, setSensorData] = useState([]);

    useEffect(() => {
        var label = props.label;
        fetch('http://'+props.api_ip+'/sensor/'+props.label)
            .then(res => res.json())
            .then(
                (data) =>{
                    setIsLoaded(true);
                    setSensorData(data);
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
        return(
            <div className="card-element">
            <div  className="card-element-heading">
                <label>{props.label}</label>
                <div className="card-element-divider"></div>
            </div>

            <div className="sensor-node-data-container">
                    <label className="card-element-label">Light </label>
                    <label className="card-element-text">Loading...</label>

                    <label className="card-element-label">Temperature </label>
                    <label className="card-element-text">Loading...</label>

                    <label className="card-element-label">Humidity </label>
                    <label className="card-element-text">Loading...</label>
            </div>
        </div>
        )
    } else {
        return(
            <div className="card-element">
                <div  className="card-element-heading">
                    <label>{props.label}</label>
                    <div className="card-element-divider"></div>
                </div>

                <div className="sensor-node-data-container">
                        <label className="card-element-label">Light </label>
                        <label className="card-element-text">{sensorData.light}</label>

                        <label className="card-element-label">Temperature </label>
                        <label className="card-element-text">{sensorData.temperature}</label>

                        <label className="card-element-label">Humidity </label>
                        <label className="card-element-text">{sensorData.humidity}</label>
                </div>
            </div>
        )
    }
}


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
            <div>
                <label>Sensor Nodes</label>
                <br/>
                <select>
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

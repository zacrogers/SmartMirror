import React, {useState, useEffect} from 'react';
import { strFirstUpper } from '../helpers';
import './myStyles.css';
import { SensorNodeList } from './SensorNodeList';

export const NodeInfo = (props) => {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [sensorInfo, setSensorInfo] = useState([]);
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

    const selectedNodeChanged = (e) =>{
        var url = 'http://'+props.api_ip+'/manage_node/'+e.target.value
        fetch(url=url, {method:"GET"})
            .then(res => res.json())
            .then(
                (data) =>{
                    setIsLoaded(true);
                    setSensorInfo(data);
                },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            )
    }

    if(error){
        return <div>Error: {error.message}</div>
    } else if (!isLoaded){
        return(
            <div className="card-element">
                <div  className="card-element-heading">
                    <label>Node Info</label>
                    <div className="card-element-divider"></div>
                </div>

                <div className="node-info-container ">
                    <label className="card-element-label">Label </label>
                    <label className="card-element-text">Loading...</label>

                    <label className="card-element-label">Type </label>
                    <label className="card-element-text">Loading...</label>

                    <label className="card-element-label">IP </label>
                    <label className="card-element-text">Loading...</label>
                </div>
            </div>
        )
    } else {
        return(
            <div className="card-element">
                <div  className="card-element-heading">
                    <label>Node Info</label>
                    <div className="card-element-divider"></div>
                </div>

                <div className="node-info-container ">
                    <label className="card-element-label">Label </label>
                    <select
                        className="node-form-inputs"
                        defaultValue={""}
                        onChange={e => selectedNodeChanged(e)}
                    >
                        {Object.values(sensorLabels).map(label=>
                            <option>
                                {label}
                            </option>
                        )}
                    </select>

                    <label className="card-element-label">Type </label>
                    <label className="card-element-text">{sensorInfo.node_type}</label>

                    <label className="card-element-label">IP </label>
                    <label className="card-element-text">{sensorInfo.ip_addr}</label>
                </div>
            </div>
        )
    }
}

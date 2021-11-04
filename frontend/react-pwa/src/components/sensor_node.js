import React, {useState, useEffect} from 'react';

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
        return <div> Loading...</div>
    } else {
        return(
            <div>
                <ul>
                    <div>
                    {
                        Object.entries(sensorData).map(
                            ([key, value]) =>
                            // <h1>{key}</h1>
                            <li key={key}>{key}:{value}</li>
                    )}
                    </div>
                </ul>
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
                <ul>
                    {Object.values(sensorLabels).map(label=>
                        <li>
                            {label}
                        </li>
                    )}
                </ul>
            </div>
        )
    }
}

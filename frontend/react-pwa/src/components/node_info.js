import React, {useState, useEffect} from 'react';
import { strFirstUpper } from '../helpers';


export const NodeInfo = (props) => {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [sensorInfo, setSensorInfo] = useState([]);

    useEffect(() => {
        var url = 'http://'+props.api_ip+'/manage_node/'+props.label
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
                    {Object.entries(sensorInfo)
                        .filter(([key]) => key !== "id") // Ignore node id for displaying
                        .map(
                            ([key, value]) =>
                            <li key={key}>{key}:{strFirstUpper(value)}</li>
                        )
                    }
                    </div>
                </ul>
            </div>
        )
    }
}

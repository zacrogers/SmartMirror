import React, {useState, useEffect} from 'react';


const SensorNode = () => {

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    // const [sensorInfo, setSensorInfo] = useState([]);
    const [sensorLabels, setSensorLabels] = useState({});

    useEffect(() => {
        var url = new URL("http://127.0.0.1:5000/node_info")
        var params = {"get_all_labels":0}
        url.search = new URLSearchParams(params).toString();

        fetch('http://127.0.0.1:5000/node_info', {'get_all_labels':0})
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

    // console.log(sensorLabels)

    if(error){
        return <div>Error: {error.message}</div>
    } else if (!isLoaded){
        return <div> Loading...</div>
    } else {

        return(
            <div>
                <ul>
                    {Object.values(sensorLabels).map(label=>
                    <li>{label}</li>)
                    /* {sensorLabels.products.map((label) =>(
                        <li key={label.id}>
                           {label.name}
                        </li>
                    ))} */}
                </ul>
            </div>
        )
    }
}


export default SensorNode;

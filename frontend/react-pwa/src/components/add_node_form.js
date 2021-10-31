import React, {useState, useEffect} from 'react';

const nodeTypes = ["Sensor", ];

export const AddNodeForm = (props) => {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [nodeTypes, setNodeTypes] = useState(null);

    useEffect(() => {
        fetch('http://127.0.0.1:5000/node_info?'+new URLSearchParams({'get_node_types':1}))
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

    console.log(nodeTypes);

    if(error){
        return <div>Error: {error.message}</div>
    } else if (!isLoaded){
        return <div> Loading...</div>
    } else {
        return(
            <div>
                <ul>
                    {Object.values(nodeTypes).map(nodeType=>
                            <li>
                                {nodeType}
                            </li>
                        )}
                </ul>
            </div>
        )
    }
}

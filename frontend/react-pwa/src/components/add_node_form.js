import React, {useState, useEffect} from 'react';


export const AddNodeForm = () => {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [nodeTypes, setNodeTypes] = useState({});

    useEffect(() => {
        fetch('http://127.0.0.1:5000/node_info?'+new URLSearchParams({'get_node_types':1}))
            .then(res => res.json())
            .then(
                (data) =>{
                    setIsLoaded(true);
                    setNodeTypes(data);
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
                <form>
                    <label>Label:</label>
                    <input
                        name="nodeLabelInput"
                        type="text"/>
                    <br/>

                    <label>Type:</label>
                    <select>
                        {Object.values(nodeTypes).map(nodeType=>
                                <option>
                                    {nodeType}
                                </option>
                            )}
                    </select>
                    <br/>

                    <label>IP:</label>
                    <input
                        name="ipAddressInput"
                        type="text"/>
                    <br/>
                    <button>Add Node</button>
                </form>
            </div>
        )
    }
}

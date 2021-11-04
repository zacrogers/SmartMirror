import React, {useState, useEffect} from 'react';


export const AddNodeForm = (props) => {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [nodeTypes, setNodeTypes] = useState({});

    useEffect(() => {
        var params = new URLSearchParams({'get_node_types':1})
        fetch('http://'+props.api_ip+'/node_info?'+params)
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

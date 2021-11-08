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

    // if(error){
    //     return (
    //         <div>
    //             <form>
    //                 <label>Add Node</label>
    //                 <br/>

    //                 <label>Label:</label>
    //                 <input
    //                     name="nodeLabelInput"
    //                     type="text"
    //                     disabled="true"/>
    //                 <br/>

    //                 <label>Type:</label>
    //                 <select disabled="true">
    //                     <option>Not Connected</option>
    //                 </select>
    //                 <br/>

    //                 <label>IP:</label>
    //                 <input
    //                     name="ipAddressInput"
    //                     type="text"
    //                     disabled="true"/>
    //                 <br/>
    //                 <button disabled="true">Add Node</button>
    //             </form>
    //         </div>
    //     )
    // } else if (!isLoaded){
    //     return <div> Loading...</div>
    // } else {
        return(
            <div>
                <form>
                    <label>Add Node</label>
                    <br/>

                    <label>Label:</label>
                    <input
                        name="nodeLabelInput"
                        type="text"
                        disabled={error ? "true":"false"}/>
                    <br/>

                    <label>Type:</label>
                    <select disabled={error ? "true":"false"}>
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
                        type="text"
                        disabled={error ? "true":"false"}/>
                    <br/>

                    {error
                        ? <button onClick={()=>{alert("API not connected")}}>Add Node</button>
                        : <button onClick={()=>{alert("API connected")}}>Add Node</button>
                    }
                </form>
            </div>
        )
    // }
}

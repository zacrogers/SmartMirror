import React, {useState, useEffect} from 'react';
import { strFirstUpper } from '../helpers';
import './myStyles.css';

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
            <div className="card-element">
                <label className="node-form-inputs">Add Node</label>
                <form>
                    <div  className="node-form-container">
                    <label className="node-form-label" for="nodeLabelInput">Label:</label>
                    <input
                        name="nodeLabelInput"
                        id="nodeLabelInput"
                        className="node-form-inputs"
                        type="text"
                        // disabled={error ? "true":"false"}
                        />

                    <label className="node-form-label">Type:</label>
                    <select className="node-form-inputs">
                        {/* <select disabled={error ? "true":"false"}> */}
                        {Object.values(nodeTypes).map(nodeType=>
                                <option>
                                    {strFirstUpper(nodeType)}
                                </option>
                        )}
                    </select>

                    <label className="node-form-label">IP:</label>
                    <input
                        name="ipAddressInput"
                        className="node-form-inputs"
                        type="text"
                        disabled={error ? "true":"false"}/>
                    </div>

                    {error
                        ? <button onClick={()=>{alert("API not connected")}}>Add Node</button>
                        : <button onClick={()=>{alert("API connected")}}>Add Node</button>
                    }
                </form>
            </div>
        )
    // }
}

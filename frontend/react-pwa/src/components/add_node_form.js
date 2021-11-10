import React, { useEffect, useState } from 'react';
import {Button} from "@mui/material"
import { strFirstUpper } from '../helpers';
import './myStyles.css';

export const AddNodeForm = (props) => {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [nodeTypes, setNodeTypes] = useState({});
    const [type, setType] = useState(null);

    const [formFields, setFormFields] = useState({
        label:"",
        type:"",
        ip_addr:""
    });

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

    const submitNode = (event) =>{
        const name = event.target.name;
        const value = event.target.value;
        setFormFields(values =>({...values, [name]: value}));

        var params = new URLSearchParams(formFields)
        var url = 'http://'+props.api_ip+'/manage_node/'+formFields.label

        alert(url+'?'+params);
        fetch(
            url=url+'?'+params,
            {method:"PUT"})
            .then(
                res => res.json()
            )
            .then(
                alert(data)
            )

            // .then(
            //     (data) =>{
            //         setIsLoaded(true);
            //         setNodeTypes(data);
            //     },
            //     (error) => {
            //         setIsLoaded(true);
            //         setError(error);
            //     }
            // )
    }

    const updateType = (event)=>
    {
        setType(event.target.value);
    }

    const onChange = (name) =>{
        return({target:{value}}) => {
            setFormFields(oldValues => ({...oldValues, [name]:value}));
        }
    }

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
                <div className="card-element-heading">
                    <label >Add Node</label>
                    <div className="card-element-divider"></div>
                </div>

                <form onSubmit={submitNode}>
                    <div  className="node-form-container">
                    <label className="node-form-label" for="nodeLabelInput">Label</label>
                    <input
                        name="label"
                        id="nodeLabelInput"
                        className="node-form-inputs"
                        type="text"
                        value={formFields.label}
                        onChange={onChange("label")}
                        // disabled={error ? "true":"false"}
                        />

                    <label className="node-form-label">Type</label>

                    <select
                        name="type"
                        className="node-form-inputs"
                        value={formFields.type}
                        onChange={onChange("type")}
                    >
                        {/* <select disabled={error ? "true":"false"}> */}
                        {Object.values(nodeTypes).map(nodeType=>
                                <option value={strFirstUpper(nodeType)}>
                                    {strFirstUpper(nodeType)}
                                </option>
                        )}
                    </select>

                    <label className="node-form-label">IP</label>
                    <input
                        name="ip_addr"
                        className="node-form-inputs"
                        type="text"
                        value={formFields.ip_addr}
                        onChange={onChange("ip_addr")}
                        pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$"
                        // disabled={error ? "true":"false"}
                        />
                    </div>

                    <button
                        className="node-form-button"
                        type="submit"
                    >
                        Add Node
                    </button>

                    {/* {error
                        ? <button className="node-form-button" onClick={()=>{alert("API not connected")}}>Add Node</button>
                        : <button className="node-form-button" onClick={()=>{alert("API connected")}}>Add Node</button>
                    } */}
                </form>
            </div>
        )
    // }
}

import React from 'react';
import { AddNodeForm } from '../components/add_node_form';


export const SettingsPage = (props) =>{

    return(
        <div name="content-container" style={{marginTop:80}}>
            <AddNodeForm api_ip={props.api_ip}/>
        </div>
    )
}

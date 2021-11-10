import React,{useState } from 'react';
import { CardRow } from '../components/cardRow';
import { NodeInfo } from '../components/nodeInfo';
import { PowerNode } from '../components/power_node';
import { SensorNodeData } from '../components/sensor_node';

import Switch from '@mui/material/Switch'


export const DashboardPage = (props) =>{
    const components = [
        <NodeInfo api_ip={props.api_ip} label="ActualBedroomSensor"/>,
        // <SensorNodeList api_ip={apiIpAddr}/>,
        <SensorNodeData api_ip={props.api_ip} label="ActualBedroomSensor"/>,
        <PowerNode label="Power Node Heading"/>,
    ];

    const [isEditable, setIsEditable] = useState(false);

    const switchChanged = () => setIsEditable(!isEditable);


    return(
        <div name="content-container" style={{marginTop:80}}>
          <CardRow elements={components}/>
          <Switch checked={isEditable} onChange={switchChanged}/>
        </div>
    )
}

import React from 'react';
import { AddNodeForm } from '../components/add_node_form';
import { CardRow } from '../components/cardRow';
import { NodeInfo } from '../components/nodeInfo';
import { PowerNode } from '../components/power_node';
import { SensorNodeData } from '../components/sensor_node';

var apiIpAddr = '192.168.1.124:5000'

const components = [
    <NodeInfo api_ip={apiIpAddr} label="ActualBedroomSensor"/>,
    // <SensorNodeList api_ip={apiIpAddr}/>,
    <SensorNodeData api_ip={apiIpAddr} label="ActualBedroomSensor"/>,
    <PowerNode label="Power Node Heading"/>,
    <AddNodeForm api_ip={apiIpAddr}/>
  ];

export const DashboardPage = () =>{

    return(
        <div name="content-container" style={{marginTop:80}}>
          <CardRow elements={components}/>
        </div>
    )
}

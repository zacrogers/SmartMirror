import React from 'react';
import logo from './logo.svg';
import './App.css';
import {SensorNodeList, SensorNodeData} from './components/sensor_node';
import { NodeInfo } from './components/node_info';
import { AddNodeForm } from './components/add_node_form';

var apiIpAddr = '127.0.0.1:5000'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <NodeInfo api_ip={apiIpAddr} label="ActualBedroomSensor"/>
        <NodeInfo api_ip={apiIpAddr} label="BedroomSensor1"/>
        <NodeInfo api_ip={apiIpAddr} label="BedroomSensor"/>
        <SensorNodeList api_ip={apiIpAddr}/>
        <SensorNodeData api_ip={apiIpAddr} label="ActualBedroomSensor"/>
        <AddNodeForm api_ip={apiIpAddr}/>
      </header>
    </div>
  );
}

export default App;

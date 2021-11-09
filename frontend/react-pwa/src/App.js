import React from 'react';
import MiniDrawer from './components/menu'
import logo from './logo.svg';
import './App.css';
import {SensorNodeList, SensorNodeData} from './components/sensor_node';
import { NodeInfo } from './components/nodeInfo';
import { AddNodeForm } from './components/add_node_form';
import { Login } from './pages/Login';
import { PowerNode } from './components/power_node';
import { CardRow } from './components/cardRow';

// var apiIpAddr = '127.0.0.1:5000'
var apiIpAddr = '192.168.1.124:5000'

function App() {
  const components = [
    <NodeInfo api_ip={apiIpAddr} label="ActualBedroomSensor"/>,
    // <SensorNodeList api_ip={apiIpAddr}/>,
    <SensorNodeData api_ip={apiIpAddr} label="ActualBedroomSensor"/>,
    <PowerNode label="Power Node Heading"/>,
    <AddNodeForm api_ip={apiIpAddr}/>
  ];

  return (
    <div className="App">
      <header className="App-header">
        <div>
          <MiniDrawer/>
        </div>
        <div name="content-container" style={{marginTop:80}}>
          <CardRow elements={components}/>
        </div>
      </header>
    </div>
  );
}

export default App;

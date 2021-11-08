import React from 'react';
import MiniDrawer from './components/menu'
import logo from './logo.svg';
import './App.css';
import {SensorNodeList, SensorNodeData} from './components/sensor_node';
import { NodeInfo } from './components/node_info';
import { AddNodeForm } from './components/add_node_form';
import { Login } from './pages/Login';
import { PowerNode } from './components/power_node';

var apiIpAddr = '127.0.0.1:5000'

function App() {
  return (
    <div className="App">
      <MiniDrawer/>
      <header className="App-header">
        <NodeInfo api_ip={apiIpAddr} label="ActualBedroomSensor"/>
        <SensorNodeList api_ip={apiIpAddr}/>
        <SensorNodeData api_ip={apiIpAddr} label="ActualBedroomSensor"/>
        <PowerNode/>
        <AddNodeForm api_ip={apiIpAddr}/>
        {/* <Login/> */}
      </header>
    </div>
  );
}

export default App;

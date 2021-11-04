import React from 'react';
import logo from './logo.svg';
import {SensorNodeList, SensorNodeData} from './components/sensor_node';
import './App.css';
import { AddNodeForm } from './components/add_node_form';

var apiIpAddr = '127.0.0.1:5000'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <SensorNodeList/>
        <SensorNodeData api_ip={apiIpAddr} label="ActualBedroomSensor"/>
        <AddNodeForm api_ip={apiIpAddr}/>
      </header>
    </div>
  );
}

export default App;

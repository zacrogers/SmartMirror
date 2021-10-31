import React from 'react';
import logo from './logo.svg';
import {SensorNodeList, SensorNodeData} from './components/sensor_node';
import './App.css';
import { AddNodeForm } from './components/add_node_form';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <SensorNodeList/>
        {/* <SensorNodeData label="BedroomSensor1"/> */}
        <AddNodeForm/>
      </header>
    </div>
  );
}

export default App;

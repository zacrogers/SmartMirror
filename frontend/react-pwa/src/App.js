import React from 'react';
import { BrowserRouter, Routes, Route} from 'react-router-dom';
import MiniDrawer from './components/menu'
import logo from './logo.svg';
import './App.css';
import {SensorNodeList, SensorNodeData} from './components/sensor_node';
import { NodeInfo } from './components/nodeInfo';
import { AddNodeForm } from './components/add_node_form';
import { Login } from './pages/Login';
import { PowerNode } from './components/power_node';
import { CardRow } from './components/cardRow';
import { SettingsPage } from './pages/SettingsPage';
import { DashboardPage } from './pages/DashboardPage';

// var apiIpAddr = '127.0.0.1:5000'
var apiIpAddr = '192.168.1.124:5000'

function App() {
  const components = [
    <NodeInfo api_ip={apiIpAddr} label="ActualBedroomSensor"/>,
    <SensorNodeData api_ip={apiIpAddr} label="ActualBedroomSensor"/>,
    <PowerNode label="Power Node Heading"/>,
    <AddNodeForm api_ip={apiIpAddr}/>
  ];

  // const links = {
  //   "Dashboard": "/dashboard",
  //   "Settings":
  // };

  return (
    <div className="App">
      <header className="App-header">
        <div>
          <MiniDrawer/>
        </div>
        <Routes>
          <Route path="/dashboard" element={<DashboardPage/>}/>
          <Route path="/settings" element={<SettingsPage/>}/>
        </Routes>
      </header>
    </div>
  );
}

export default App;

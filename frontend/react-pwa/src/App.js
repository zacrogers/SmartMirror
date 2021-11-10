import React from 'react';
import { Route, Routes } from 'react-router-dom';
import './App.css';
import { AddNodeForm } from './components/add_node_form';
import MiniDrawer from './components/menu';
import { NodeInfo } from './components/nodeInfo';
import { PowerNode } from './components/power_node';
import { SensorNodeData } from './components/sensor_node';
import { DashboardPage } from './pages/DashboardPage';
import { SettingsPage } from './pages/SettingsPage';

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
          <Route
            path="/dashboard"
            element={<DashboardPage api_ip={apiIpAddr}/>}
          />
          <Route
            path="/settings"
            element={<SettingsPage api_ip={apiIpAddr}/>}
          />
        </Routes>
      </header>
    </div>
  );
}

export default App;

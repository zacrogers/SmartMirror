import requests
import json
from typing import Dict
from ipaddress import IPv4Address
from node_types import DoorLockNode, Node, NodeType, PowerStripNode, SensorNode
API_IP_ADDRESS = "127.0.0.1:5000"

def set_ip_address(ip:IPv4Address, port:int) -> None:
    global API_IP_ADDRESS
    API_IP_ADDRESS = f"{str(ip)}:{port}"


def get_sensor_nodes() -> Dict[str, SensorNode]:
    raise NotImplementedError


def get_power_nodes() -> Dict[str, PowerStripNode]:
    raise NotImplementedError


def get_lock_nodes() -> Dict[str, DoorLockNode]:
    raise NotImplementedError


def add_node(name:str, ip_addr:IPv4Address, type:NodeType) -> bool:
    raise NotImplementedError


def delete_node(name:str) -> bool:
    try:
        response = requests.delete(f"http://{API_IP_ADDRESS}/node_delete/{name}")
        status = response.status_code

        if status == 200:
            return True

        elif status == 404:
            return False

    except Exception as e:
        return e


def update_node_name(name:str) -> bool:
    raise NotImplementedError


def update_node_ip(name:str, ip:IPv4Address) -> bool:
    raise NotImplementedError


def get_sensor_values(name:str) -> Dict[str, float]:
    ''' Get values from sensor node as json object. Returns empty json object if node doesn't exist.'''
    try:
        response = requests.get(f"http://{API_IP_ADDRESS}/sensor/{name}")
        status = response.status_code

        if status == 200:
            return response.json()

        elif status == 204:
            return json.dumps({})

    except Exception as e:
        return e


def power_on(name:str, channel:int) -> None:
    raise NotImplementedError


def power_off(name:str, channel:int) -> None:
    raise NotImplementedError

# BASE = "http://127.0.0.1:5000"
# resp = requests.get(BASE + "/node/BedroomSensor/195.1.2.6/SENSOR")

# print(resp)

# nt = "SENSOR"

# print(NodeType["SENSOR"].name)


print(get_sensor_values("BedroomSensor"))
# print(delete_node("BedroomSensor"))
# print(get_sensor_values("BedroomSensor"))


# s = SensorNode("sensors", IPv4Address("192.0.0.1"))
# data = s.get_data()
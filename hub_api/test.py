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


def add_node(label:str, ip_addr:IPv4Address, node_type:NodeType) -> bool:
    try:
        # response = requests.put(f"http://{API_IP_ADDRESS}/node/{label}/{ip_addr}/{node_type.name}")
        response = requests.put(f"http://{API_IP_ADDRESS}/manage_node/{label}", {"label":label, "ip_addr":str(ip_addr), "type":str(node_type.name)})

        status = response.status_code

        if status == 201:
            return True

        elif status == 400:
            return False

        elif status == 409:
            return False

    except Exception as e:
        return e



def delete_node(name:str) -> bool:
    try:
        response = requests.delete(f"http://{API_IP_ADDRESS}/manage_node/{name}")
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


print(add_node("LoungeSensor", IPv4Address("192.0.99.1"), NodeType.SENSOR))
print(add_node("BedroomSensor", IPv4Address("192.1.2.3"), NodeType.SENSOR))
print(add_node("KitchenSensor", IPv4Address("192.2.2.3"), NodeType.SENSOR))

# print(delete_node("LoungeSensor"))
# print(delete_node("BedroomSensor"))
# print(delete_node("KitchenSensor"))

print(get_sensor_values("LoungeSensor"))
print(get_sensor_values("BedroomSensor"))
print(get_sensor_values("KitchenSensor"))


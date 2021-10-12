import requests
import json
from typing import Dict, List
from ipaddress import IPv4Address
from node_types import DoorLockNode, Node, NodeType, PowerStripNode, SensorNode

API_IP_ADDRESS = "127.0.0.1:5000"


def set_ip_address(ip: IPv4Address, port: int) -> None:
    global API_IP_ADDRESS
    API_IP_ADDRESS = f"{str(ip)}:{port}"


""" 
    Node management methods
"""


def get_sensor_nodes() -> Dict[str, SensorNode]:
    raise NotImplementedError


def get_power_nodes() -> Dict[str, PowerStripNode]:
    raise NotImplementedError


def get_lock_nodes() -> Dict[str, DoorLockNode]:
    raise NotImplementedError


def get_nodes() -> Dict[str, NodeType]:
    raise NotImplementedError


def get_node_labels() -> List[str]:
    raise NotImplementedError


def get_node(label: str) -> Node:
    try:
        response = requests.get(f"http://{API_IP_ADDRESS}/manage_node/{label}")

        status = response.status_code

        if status == 200:
            fields = response.json()

            if fields["node_type"].upper() == NodeType.SENSOR.name:
                return SensorNode(fields["label"], IPv4Address(fields["ip_addr"]))

            elif fields["node_type"].upper() == NodeType.POWER.name:
                return PowerStripNode(fields["label"], IPv4Address(fields["ip_addr"]))

            elif fields["node_type"].upper() == NodeType.DOOR_LOCK.name:
                return DoorLockNode(fields["label"], IPv4Address(fields["ip_addr"]))

            else:
                return None

    except Exception as e:
        return e


def add_node(label: str, ip_addr: IPv4Address, node_type: NodeType) -> bool:
    try:
        node = {"label": label, "ip_addr": str(ip_addr), "type": str(node_type.name)}
        response = requests.put(f"http://{API_IP_ADDRESS}/manage_node/{label}", node)

        status = response.status_code

        if status == 201:
            return True

        elif status == 400:
            return False

        elif status == 409:
            return False

    except Exception as e:
        return e


def delete_node(name: str) -> bool:
    try:
        response = requests.delete(f"http://{API_IP_ADDRESS}/manage_node/{name}")
        status = response.status_code

        if status == 200:
            return True

        elif status == 404:
            return False

    except Exception as e:
        return e


def update_node(label: str, new_label: str, new_ip_addr: IPv4Address = None) -> bool:
    try:
        if new_ip_addr:
            args = {"label": new_label, "ip_addr": str(new_ip_addr)}
        else:
            args = {"label": new_label}

        response = requests.patch(f"http://{API_IP_ADDRESS}/manage_node/{label}", args)

        status = response.status_code

        if status == 200:
            return True

        elif status == 400:
            return False

        elif status == 409:
            return False

    except Exception as e:
        return e


""" 
    Sensor node methods 
"""


def get_sensor_values(name: str) -> Dict[str, float]:
    """Get values from sensor node as json object. Returns empty json object if node doesn't exist."""
    try:
        response = requests.get(f"http://{API_IP_ADDRESS}/sensor/{name}", timeout=3)
        response.raise_for_status()
        status = response.status_code

        if status == 200:
            return response.json()

        elif status == 204:
            return json.dumps({})

    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


""" 
    Power strip node methods
"""


def power_on(label: str, channel: int) -> List[bool]:
    try:
        args = {"channel": channel, "state": True}
        response = requests.put(f"http://{API_IP_ADDRESS}/power/{label}", args)
        status = response.status_code

        if status == 200:
            return True

        elif status == 404:
            return False

    except Exception as e:
        return e


def power_off(label: str, channel: int) -> List[bool]:
    try:
        args = {"channel": channel, "state": False}
        response = requests.put(f"http://{API_IP_ADDRESS}/power/{label}", args)
        status = response.status_code

        if status == 200:
            return True

        elif status == 404:
            return False

    except Exception as e:
        return e


def get_power_states(label: str) -> List[bool]:
    raise NotImplementedError


"""
    Door lock node methods 
"""


def lock_door(label: str) -> None:
    raise NotImplementedError


def unlock_door(label: str) -> None:
    raise NotImplementedError


def get_door_lock_state(label: str) -> bool:
    raise NotImplementedError


if __name__ == "__main__":
    # print(add_node("LoungeSensor", IPv4Address("192.0.99.1"), NodeType.SENSOR))
    # print(add_node("BedroomSensor", IPv4Address("192.1.2.3"), NodeType.SENSOR))
    # print(add_node("KitchenSensor", IPv4Address("192.2.2.3"), NodeType.SENSOR))

    # print(delete_node("LoungeSensor"))
    # print(delete_node("BedroomSensor"))
    # print(delete_node("KitchenSensor"))

    # print(get_sensor_values("LoungeSensor"))
    # print(get_sensor_values("BedroomSensor"))
    # print(get_sensor_values("KitchenSensor"))

    print(get_sensor_values("LoungeSensor1"))

    # print(update_node("LoungeSensor", "LoungeSensor1"))

    # print(get_sensor_values("LoungeSensor1"))

from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import List
from ipaddress import IPv4Address
import requests
import json
from bs4 import BeautifulSoup

class NodeType(Enum):
    BASE      = auto()
    SENSOR    = auto()
    POWER     = auto()
    DOOR_LOCK = auto()


class Node(ABC):
    ''' Base class for IOT Node classes '''
    def __init__(self, label:str, ip_addr:IPv4Address, node_type:NodeType=NodeType.BASE) -> None:
        self.label = label
        self.ip_addr = ip_addr
        self.node_type = node_type

    @abstractmethod
    def reset(self) -> None:
        ''' Hard reset node '''


class SensorNode(Node):
    def __init__(self, label:str, ip_addr:IPv4Address) -> None:
        super().__init__(label, ip_addr, NodeType.SENSOR)

    def get_data(self) -> dict:
        ''' Fetches light, temperature and humidity data from web server as json'''
        try:
            data = requests.get(f"http://{str(self.ip_addr)}")
            print(f"Status code for sensor node:{data.status_code}")

            if(data.status_code == 200):
                soup = BeautifulSoup(data.text, 'html.parser')
                table = soup.find("table", class_="sensor_values")
                headers = [header.text for header in table.findAll("th")]
                values = [{headers[i]: cell.text for i, cell in enumerate(row.find_all('td'))}
                            for row in table.find_all('tr')]

                vals = list(values[1].values()) #  First row in list is empty so only return second
                return {"light":vals[0], "temperature":vals[1], "humidity":vals[2]}

        except Exception as e:
            print(e)
            return {"light":0, "temperature":0, "humidity":0}

    def reset(self) -> None:
        return NotImplementedError


class PowerStripNode(Node):
    def __init__(self, label:str, ip_addr:IPv4Address) -> None:
        super().__init__(label, ip_addr, NodeType.POWER)
        self.num_chans = 4

    def channel_on(self, channel:int) -> None:
        return NotImplementedError

    def channel_off(self, channel:int) -> None:
        return NotImplementedError

    def all_on(self) -> None:
        for i in range(0, self.num_chans-1):
            self.channel_on(i)

    def all_off(self) -> None:
        for i in range(0, self.num_chans-1):
            self.channel_off(i)

    def get_states(self) -> List[bool]:
        return NotImplementedError

    def reset(self) -> None:
        return NotImplementedError


class DoorLockNode(Node):
    def __init__(self, label: str, ip_addr: IPv4Address) -> None:
        super().__init__(label, ip_addr, NodeType.DOOR_LOCK)

    def unlock(self) -> None:
        return NotImplementedError

    def lock(self) -> None:
        return NotImplementedError

    def get_state(self) -> bool:
        return NotImplementedError

    def reset(self) -> None:
        return NotImplementedError



d = DoorLockNode("name", IPv4Address("192.1.2.6"))    

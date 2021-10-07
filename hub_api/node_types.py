from enum import Enum, auto
from abc import ABC, abstractmethod
from ipaddress import IPv4Address

class NodeType(Enum):
    BASE = auto()
    SENSOR = auto()
    POWER = auto()
    DOOR_LOCK = auto()


class Node(ABC):
    ''' Base class for IOT Node classes '''
    def __init__(self, label:str, ip_addr:IPv4Address, node_type:NodeType=NodeType.BASE) -> None:
        self.label = label
        self.ip_addr = ip_addr
        self.node_type = node_type

    @abstractmethod
    def reset(self) -> None:
        ''' Hard reset device '''
        return NotImplementedError


class SensorNode(Node):
    def __init__(self, label:str, ip_addr:IPv4Address) -> None:
        super().__init__(label, ip_addr, NodeType.SENSOR)

    def get_data(self) -> dict:
        ''' Return sensor values as json '''
        return NotImplementedError

    def reset(self)-> None:
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

    def get_states(self) -> dict:
        return NotImplementedError

    def reset(self)-> None:
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

    def reset(self)-> None:
        return NotImplementedError



    
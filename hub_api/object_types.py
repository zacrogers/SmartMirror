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
    def reset(self):
        return NotImplementedError


class SensorNode(Node):
    def __init__(self, label:str, ip_addr:IPv4Address) -> None:
        super().__init__(label, ip_addr, NodeType.SENSOR)

    def get_data(self):
        return NotImplementedError

    def reset(self):
        return NotImplementedError


class PowerStripNode(Node):
    def __init__(self, label:str, ip_addr:IPv4Address, num_chans:int=4) -> None:
        super().__init__(label, ip_addr, NodeType.POWER)
        self.num_chans = num_chans

    def channel_on(self, channel:int):
        return NotImplementedError

    def channel_off(self, channel:int):
        return NotImplementedError

    def all_on(self, channel:int) -> None:
        for i in range(0, self.num_chans-1):
            self.channel_on(i)

    def all_off(self, channel:int) -> None:
        for i in range(0, self.num_chans-1):
            self.channel_off(i)

    def get_states(self):
        return NotImplementedError

    def reset(self):
        return NotImplementedError


class DoorLockNode(Node):
    def __init__(self, label: str, ip_addr: IPv4Address) -> None:
        super().__init__(label, ip_addr, NodeType.DOOR_LOCK)

    def unlock(self):
        return NotImplementedError

    def lock(self):
        return NotImplementedError

    def get_state(self) -> bool:
        return NotImplementedError

    def reset(self):
        return NotImplementedError


d = SensorNode("Node", IPv4Address("127.168.2.1"))
print(d)

    
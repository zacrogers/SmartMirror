from node_types import DoorLockNode, Node, NodeType, PowerStripNode, SensorNode


n = SensorNode("ThisLabel", "192.168.1.72")

print(n.get_data())

import requests
import json
from ipaddress import IPv4Address
from node_types import SensorNode
BASE = "http://127.0.0.1:5000/"

resp = requests.get(BASE + "/sensor/BedroomSensor")

print(resp.json())

# s = SensorNode("sensors", IPv4Address("192.0.0.1"))
# data = s.get_data()
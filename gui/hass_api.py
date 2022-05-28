from pprint import pprint
from time import time
import requests
import json
from datetime import datetime

ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI1ZDNlYzc2YWRjMTA0MTIxOTRjMWM4MzNlOWUzM2U5ZCIsImlhdCI6MTY1MzE3OTcxOSwiZXhwIjoxOTY4NTM5NzE5fQ.I60rwrJVfPF4fVhXf0PtpAqe6R0s_oHmhZV950K8U9w"


class HassApi:
    def __init__(self, ip_addr="192.168.68.63", port=8123):
        self.ip_addr = ip_addr
        self.port = port

    def get_sensor_current_val(self, entity_id: str):
        url = f"http://{self.ip_addr}:{self.port}/api/states/{entity_id}"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "content-type": "application/json",
        }
        data = requests.get(url, headers=headers)
        content = json.loads(data.content)
        name = content.get("attributes", {}).get("friendly_name")
        val = content.get("state")

        return name, val

    def get_sensor_last_day(self, entity_id: str):
        url = f"http://{self.ip_addr}:{self.port}/api/history/period"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "content-type": "application/json",
        }
        params = {"filter_entity_id": entity_id, "minimal_response": True}
        data = requests.get(url, headers=headers, params=params)
        content = json.loads(data.content)
        name = content[0][0].get("attributes", {}).get("friendly_name")
        vals = {"name": name, "values": []}

        for state in content[0]:
            timestamp = self._clean_timestamp(state.get("last_changed"))
            vals["values"].append({"timestamp": timestamp, "value": state.get("state")})

        return vals

    def _clean_timestamp(self, timestamp: str) -> datetime:
        ts = timestamp.replace("T", " ")
        ts = ts.split("+")[0]
        return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")


if __name__ == "__main__":
    hass_api = HassApi()
    print(hass_api.get_sensor_current_val("sensor.fgf"))

    # pprint(hass_api.get_sensor_last_day("sensor.temperature"))

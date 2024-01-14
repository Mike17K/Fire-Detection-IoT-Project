import requests
import json
from uuid import uuid4
from datetime import datetime

from typing import Dict, Tuple


class ContextBroker:
    def __init__(self, context_broker_host):
        self.context_broker_base_url = f"http://{context_broker_host}:1026/v2/entities"

    def create_tree_sensor(self, deviceId, location:Tuple[float, float]) -> None:
        data = {
            "id": deviceId,
            "type": "Device",
            "controlledProperty": {
                "type": "List",
                "value":["CO2", "humidity", "temperature"]
            },
            "dateObserved": {
                "type": "DateTime",
                "value": None
            },
            "location": {
                "type": "GeoProperty",
                "value": {
                    "type": "Point",
                    "coordinates": [location[0], location[1]]
                }
            },
            "serialNumber": {
                "type": "Text",
                "value": str(uuid4()),
            },
            "value": {
                "type": "Text",
            }
        }

        payload = json.dumps(data)

        print(f"Creating tree sensor: {data['id']}", end='...')

        response = requests.post(
            self.context_broker_base_url,
            data=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code != 201:
            print("Fail")
            raise Exception(f"{response.status_code} {response.text}")

        print("Success")


    def update_tree_sensor_value(
        self,
        deviceId:str,
        dateObserved:datetime,
        CO2:str|None = None,
        humidity:str|None = None,
        temperature:str|None = None,
    ) -> None:

        if not CO2:
            CO2 = ""
        if not humidity:
            humidity = ""
        if not temperature:
            temperature = ""

        payload = json.dumps({
            "dateObserved": {
                "type": "DateTime",
                "value": dateObserved.isoformat()
            },
            "value": {
                "type": "Text",
                "value": f"{CO2}&{humidity}&{temperature}"
            }
        })

        print(f"Updating tree sensor: {deviceId}", end='...')

        response = requests.patch(
            f"{self.context_broker_base_url}/{deviceId}/attrs",
            data=payload,
            headers={"Content-Type": "application/json"}
        )


        if response.status_code != 204:
            print("Fail")
            raise Exception(f"{response.status_code} {response.text}")

        print("Success")


    def get_tree_sensor(self, deviceId:str) -> Dict[str, str]:

        response = requests.get(
            f"{self.context_broker_base_url}/{deviceId}",
            headers={"Accept": "application/json"},
            params={"options": "keyValues"}
        )

        if response.status_code != 200:
            raise Exception(f"{response.status_code} {response.text}")

        return response.json()

    def delete_tree_sensor(self, deviceId:str) -> None:

        print(f"Deleting tree sensor: {deviceId}", end='...')

        response = requests.delete(
            f"{self.context_broker_base_url}/{deviceId}",
            headers={"Accept": "application/json"}
        )

        if response.status_code != 204:
            print("Fail")
            raise Exception(f"{response.status_code} {response.text}")

        print("Success")

if __name__ == "__main__":
    context = ContextBroker("192.168.1.2")

    context.create_tree_sensor("tree_sensor_0", (0,0))

    print(context.get_tree_sensor("tree_sensor_0"))

    context.update_tree_sensor_value(
        "tree_sensor_0",
        datetime.utcnow(),
        CO2="15",
        humidity="15",
        temperature="15"
    )

    print(context.get_tree_sensor("tree_sensor_0"))

    context.delete_tree_sensor("tree_sensor_0")

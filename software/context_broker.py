import requests
import json
from uuid import uuid4
from datetime import datetime

from typing import Dict, Tuple, List


class ContextBroker:
    def __init__(self, context_broker_host):
        self.context_broker_base_url = f"http://{context_broker_host}:1026/v2/entities"

    def __create_sensor(self, type:str, deviceId:str, location:Tuple[float, float], serialNumber:str) -> None:
        data = {
            "id": deviceId,
            "type": "Device",
            "dateObserved": {
                "type": "DateTime",
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
                "value": serialNumber,
            },
            "value": {
                "type": "Text",
            }
        }

        if type == "tree_sensor":
            data["controlledProperty"] = {
                "type": "List",
                "value":["CO2", "humidity", "temperature"]
            }
        elif type == "wind_sensor":
            data["controlledProperty"] = {
                "type": "List",
                "value":["windDirection", "windSpeed"]
            }

        payload = json.dumps(data)

        response = requests.post(
            self.context_broker_base_url,
            data=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code != 201:
            print("Fail")
            raise Exception(f"{response.status_code} {response.text}")

        print("Success")

    def create_tree_sensor(self, deviceId, location:Tuple[float, float], serialNumber:str) -> None:
        print(f"Creating tree sensor: {deviceId}", end='...')
        self.__create_sensor("tree_sensor", deviceId, location, serialNumber)

    def create_wind_sensor(self, deviceId, location:Tuple[float, float], serialNumber:str) -> None:
        print(f"Creating wind sensor: {deviceId}", end='...')
        self.__create_sensor("wind_sensor", deviceId, location, serialNumber)


    def __update_sensor(
        self,
        deviceId:str,
        dateObserved:datetime,
        data: List[str]
    ) -> None:

        payload = json.dumps({
            "dateObserved": {
                "type": "DateTime",
                "value": dateObserved.isoformat()
            },
            "value": {
                "type": "Text",
                "value": "&".join(data)
            }
        })

        response = requests.patch(
            f"{self.context_broker_base_url}/{deviceId}/attrs",
            data=payload,
            headers={"Content-Type": "application/json"}
        )


        if response.status_code != 204:
            print("Fail")
            raise Exception(f"{response.status_code} {response.text}")

        print("Success")

    def update_tree_sensor(
        self,
        deviceId:str,
        dateObserved:datetime,
        CO2: str|None = None,
        humidity: str|None = None,
        temperature: str|None = None
    ) -> None:
        print(f"Updating tree sensor: {deviceId}", end='...')

        data = [
            CO2 if CO2 else "",
            humidity if humidity else "",
            temperature if temperature else ""
        ]

        self.__update_sensor(deviceId, dateObserved, data)

    def update_wind_sensor(
        self,
        deviceId:str,
        dateObserved:datetime,
        windDirection: str|None = None,
        windSpeed: str|None = None,
    ) -> None:
        print(f"Updating wind sensor: {deviceId}", end='...')

        data = [
            windDirection if windDirection else "",
            windSpeed if windSpeed else "",
        ]

        self.__update_sensor(deviceId, dateObserved, data)


    def get_sensor(self, deviceId:str) -> Dict[str, str]:

        response = requests.get(
            f"{self.context_broker_base_url}/{deviceId}",
            headers={"Accept": "application/json"},
            params={"options": "keyValues"}
        )

        if response.status_code != 200:
            raise Exception(f"{response.status_code} {response.text}")

        return response.json()

    def delete_sensor(self, deviceId:str) -> None:
        print(f"Deleting device: {deviceId}", end='...')

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

    context.create_tree_sensor("tree_sensor_0", (0,0), str(uuid4()))
    context.create_wind_sensor("wind_sensor_0", (0,0), str(uuid4()))

    print(context.get_sensor("tree_sensor_0"))

    context.update_tree_sensor(
        "tree_sensor_0",
        datetime.utcnow(),
        CO2="15",
        humidity="15",
        temperature="15"
    )

    print(context.get_sensor("tree_sensor_0"))

    print(context.get_sensor("wind_sensor_0"))

    context.update_wind_sensor(
        "wind_sensor_0",
        datetime.utcnow(),
        windDirection="15",
        windSpeed="15",
    )

    print(context.get_sensor("wind_sensor_0"))

    context.delete_sensor("tree_sensor_0")
    context.delete_sensor("wind_sensor_0")

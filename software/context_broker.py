import requests
import json
from uuid import uuid4
from datetime import datetime

from typing import Dict, Tuple, List


class ContextBroker:
    def __init__(
        self,
        context_broker_host:str
    ):

        self.context_broker_base_url = f"http://{context_broker_host}:1026/v2/entities"


    #### Create Entities ####
    def __create_entity(
        self,
        data:Dict
    ) -> None:

        response = requests.post(
            self.context_broker_base_url,
            json=data
        )

        if response.status_code != 201:
            print("Fail")
            raise Exception(f"{response.status_code} {response.text}")

        print("Success")

    def __create_sensor(
        self,
        type:str,
        deviceId:str,
        location:Tuple[float, float],
        serialNumber:str
    ) -> None:

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
                    "coordinates": location
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

        self.__create_entity(data)

    def create_tree_sensor(
        self,
        deviceId:str,
        location:Tuple[float, float],
        serialNumber:str
    ) -> None:

        print(f"Creating tree sensor: {deviceId}", end='...')
        self.__create_sensor("tree_sensor", deviceId, location, serialNumber)

    def create_wind_sensor(
        self,
        deviceId:str,
        location:Tuple[float, float],
        serialNumber:str
    ) -> None:

        print(f"Creating wind sensor: {deviceId}", end='...')
        self.__create_sensor("wind_sensor", deviceId, location, serialNumber)

    def create_fire_forest_status(
        self,
        entityId:str,
        fireDetected:bool,
        fireDetectedConfidence:float,
        fireRiskIndex:float,
        location:List[Tuple[float, float]]
    ) -> None:

        print(f"Creating FireForestStatus: {entityId}", end='...')

        data = {
            "id": entityId,
            "type": "FireForestStatus",
            "dateCreated": {
                "type": "DateTime",
                "value": datetime.utcnow().isoformat()
            },
            "fireDetected": {
                "type": "Boolean",
                "value": fireDetected
            },
            "fireDetectedConfidence": {
                "type": "Float",
                "value": fireDetectedConfidence
            },
            "fireRiskIndex": {
                "type": "Float",
                "value": fireRiskIndex
            },
        }

        if len(location) == 1:
            data["location"] = {
                "type": "GeoProperty",
                "value": {
                    "type": "Point",
                    "coordinates": location[0]
                }
            }
        else:
            data["location"] = {
                "type": "GeoProperty",
                "value": {
                    "type": "Polygon",
                    "coordinates": location
                }
            }

        self.__create_entity(data)


    #### Update Entities ####
    def __update_sensor(
        self,
        deviceId:str,
        dateObserved:datetime,
        data:List[str]
    ) -> None:

        payload = {
            "dateObserved": {
                "type": "DateTime",
                "value": dateObserved.isoformat()
            },
            "value": {
                "type": "Text",
                "value": "&".join(data)
            }
        }

        response = requests.patch(
            f"{self.context_broker_base_url}/{deviceId}/attrs",
            json=payload
        )


        if response.status_code != 204:
            print("Fail")
            raise Exception(f"{response.status_code} {response.text}")

        print("Success")

    def update_tree_sensor(
        self,
        deviceId:str,
        dateObserved:datetime,
        CO2:str|None = None,
        humidity:str|None = None,
        temperature:str|None = None
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
        windDirection:str|None = None,
        windSpeed:str|None = None,
    ) -> None:

        print(f"Updating wind sensor: {deviceId}", end='...')

        data = [
            windDirection if windDirection else "",
            windSpeed if windSpeed else "",
        ]

        self.__update_sensor(deviceId, dateObserved, data)


    #### Get Entities ####
    def get_entity(
        self,
        entityId:str,
        detailed:bool=False
    ) -> Dict[str, str]:

        params = {}
        if not detailed:
            params["options"] = "keyValues"

        response = requests.get(
            f"{self.context_broker_base_url}/{entityId}",
            headers={"Accept": "application/json"},
            params=params
        )

        if response.status_code != 200:
            raise Exception(f"{response.status_code} {response.text}")

        return response.json()


    #### Delete Entities ####
    def delete_entity(
        self,
        entityId:str
    ) -> None:

        print(f"Deleting entity: {entityId}", end='...')

        response = requests.delete(
            f"{self.context_broker_base_url}/{entityId}",
        )

        if response.status_code != 204:
            print("Fail")
            raise Exception(f"{response.status_code} {response.text}")

        print("Success")


if __name__ == "__main__":
    context = ContextBroker("192.168.1.2")

    context.create_tree_sensor("tree_sensor_0", (0,0), str(uuid4()))
    context.create_wind_sensor("wind_sensor_0", (0,0), str(uuid4()))

    print(context.get_entity("tree_sensor_0"))

    context.update_tree_sensor(
        "tree_sensor_0",
        datetime.utcnow(),
        CO2="15",
        humidity="15",
        temperature="15"
    )

    print(context.get_entity("tree_sensor_0"))

    context.delete_entity("tree_sensor_0")

    print(context.get_entity("wind_sensor_0"))

    context.update_wind_sensor(
        "wind_sensor_0",
        datetime.utcnow(),
        windDirection="15",
        windSpeed="15",
    )

    print(context.get_entity("wind_sensor_0", detailed=True))

    context.delete_entity("wind_sensor_0")

    context.create_fire_forest_status(
        "fire_forest_status_0",
        False,
        0.5,
        0.9,
        [(0,0), (0,0)]
    )

    print(context.get_entity("fire_forest_status_0"))

    context.delete_entity("fire_forest_status_0")

import requests
from uuid import uuid4
from datetime import datetime

from typing import Dict, Tuple, List, Any


class ContextBroker:
    def __init__(
        self,
        context_broker_host:str
    ):

        self.context_broker_base_url = f"http://{context_broker_host}:1026/v2"


    #### Create Entities ####
    def __create_entity(
        self,
        data:Dict[str, Any]
    ) -> None:

        response = requests.post(
            f"{self.context_broker_base_url}/entities",
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
                "type": "geo:json",
                "value": {
                    "type": "Point",
                    "coordinates": location[::-1] # fiware-orion stores locations as lon,lat instead of the common lat,lon
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
                "value":["co2", "humidity", "temperature"]
            }
        elif type == "wind_sensor":
            data["controlledProperty"] = {
                "type": "List",
                "value":["windDirection", "windSpeed"]
            }

        self.__create_entity(data)

    def __reverse_coordinates(self, entity:Dict) -> Dict:
        # convert locations from lon,lat that fiware-orion stores to the more common lat,lon

        if entity["location"]["type"] == "Point":
            entity["location"]["coordinates"] = entity["location"]["coordinates"][::-1]

        elif entity["location"]["type"] == "Polygon":
            newCoords = []
            for coord in entity["location"]["coordinates"][0]:
                newCoords.append(coord[::-1])

            entity["location"]["coordinates"] = [newCoords]

        return entity

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
            "location": {
                "type": "geo:json",
                "value": None
            }
        }

        if len(location) == 1:
            data["location"]["value"] = {
                "type": "Point",
                "coordinates": location[0][::-1] # fiware-orion stores locations as lon,lat instead of the common lat,lon
            }
        else:
            # fiware-orion stores locations as lon,lat instead of the common lat,lon
            reversedLocations = []
            for point in location:
                reversedLocations.append(point[::-1])

            data["location"]["value"] = {
                "type": "Polygon",
                "coordinates": [reversedLocations]
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
            f"{self.context_broker_base_url}/entities/{deviceId}/attrs",
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
        co2:float|None = None,
        humidity:float|None = None,
        temperature:float|None = None
    ) -> None:

        print(f"Updating tree sensor: {deviceId}", end='...')

        data = [
            str(co2) if co2 else "",
            str(humidity) if humidity else "",
            str(temperature) if temperature else ""
        ]

        self.__update_sensor(deviceId, dateObserved, data)

    def update_wind_sensor(
        self,
        deviceId:str,
        dateObserved:datetime,
        windDirection:int|None = None,
        windSpeed:float|None = None,
    ) -> None:

        print(f"Updating wind sensor: {deviceId}", end='...')

        data = [
            str(windDirection) if windDirection else "",
            str(windSpeed) if windSpeed else "",
        ]

        self.__update_sensor(deviceId, dateObserved, data)


    #### Get Entities ####
    def get_entity(
        self,
        entityId:str,
    ) -> Dict[str, Any]:

        response = requests.get(
            f"{self.context_broker_base_url}/entities/{entityId}",
            headers={"Accept": "application/json"},
            params={"options": "keyValues"}
        )

        if response.status_code != 200:
            raise Exception(f"{response.status_code} {response.text}")

        entity = response.json()
        entity = self.__reverse_coordinates(entity)

        return entity

    def get_tree_sensors(self) -> List[Dict[str, Any]]:

        response = requests.get(
            f"{self.context_broker_base_url}/entities",
            headers={"Accept": "application/json"},
            params={
                "idPattern": "tree_sensor_*",
                "limit": 1000,
                "options": "keyValues"
            }
        )

        entities = response.json()

        for i, entity in enumerate(entities):
            entities[i]["location"]["coordinates"] = entity["location"]["coordinates"][::-1]

        return entities

    def get_wind_sensors(self) -> List[Dict[str, Any]]:

        response = requests.get(
            f"{self.context_broker_base_url}/entities",
            headers={"Accept": "application/json"},
            params={
                "idPattern": "wind_sensor_*",
                "limit": 1000,
                "options": "keyValues"
            }
        )

        entities = response.json()

        for i, entity in enumerate(entities):
            entities[i]["location"]["coordinates"] = entity["location"]["coordinates"][::-1]

        return entities

    def find_device_by_serial(
        self,
        serialNumber:str
    ) -> Dict:

        response = requests.get(
            f"{self.context_broker_base_url}/entities",
            headers={"Accept": "application/json"},
            params={
                "q": f"serialNumber=={serialNumber}",
                "options": "keyValues"
            }
        )

        try:
            device = response.json()[0]
            device = self.__reverse_coordinates(device)

            return device
        except:
            return {}

    def find_devices_by_location(
        self,
        point:Tuple[float, float],
        maxDistance:int,
    ) -> Dict:

        response = requests.get(
            f"{self.context_broker_base_url}/entities",
            headers={"Accept": "application/json"},
            params={
                "georel": f"near;maxDistance:{maxDistance}",
                "geometry": "point",
                "coords": ','.join(map(str, point)),
                "options": "keyValues"
            }
        )

        devices = response.json()
        for i, device in enumerate(devices):
            devices[i] = self.__reverse_coordinates(device)

        return devices


    #### Delete Entities ####
    def delete_entity(
        self,
        entityId:str
    ) -> None:

        print(f"Deleting entity: {entityId}", end='...')

        response = requests.delete(
            f"{self.context_broker_base_url}/entities/{entityId}",
        )

        if response.status_code != 204:
            print("Fail")
            raise Exception(f"{response.status_code} {response.text}")

        print("Success")


    #### Subscriptions ####
    def subscribe_to_device_updates(self, host):
        print(f"Creating subscription", end="...")

        subscription = {
            "subject": {
                "entities": [
                    {
                        "idPattern": ".*",
                        "type": "Device"
                    }
                ]
            },
            "notification": {
                "http": {
                    "url": host
                },
                "attrsFormat": "keyValues"
            }
        }

        response = requests.post(
            f"{self.context_broker_base_url}/subscriptions",
            json=subscription,
        )

        if response.status_code != 201:
            print("Fail")
            raise Exception(f"{response.status_code} {response.text}")

        print("Success")

    def list_subscriptions(self):
        response = requests.get(
            f"{self.context_broker_base_url}/subscriptions",
        )

        subscriptions = response.json()

        return subscriptions

    def delete_subscription(self, subscription_id):
        print(f"Deleting subscription: {subscription_id}", end="...")

        response = requests.delete(
            f"{self.context_broker_base_url}/subscriptions/{subscription_id}",
        )

        if response.status_code != 204:
            print("Fail")
            raise Exception(f"{response.status_code} {response.text}")

        print("Success")


if __name__ == "__main__":
    context = ContextBroker("192.168.1.2")

    context.subscribe_to_device_updates("http://192.168.1.5:3001")

    try:
        context.create_tree_sensor("tree_sensor_0", (1,2), "test")
        context.create_wind_sensor("wind_sensor_0", (3,4), str(uuid4()))
    except:
        pass

    print(context.get_entity("tree_sensor_0"))

    context.update_tree_sensor(
        "tree_sensor_0",
        datetime.utcnow(),
        co2=15,
        humidity=15,
        temperature=15
    )

    print(context.get_entity("tree_sensor_0"))

    print(context.get_entity("wind_sensor_0"))

    context.update_wind_sensor(
        "wind_sensor_0",
        datetime.utcnow(),
        windDirection=15,
        windSpeed=15,
    )

    print(context.get_entity("wind_sensor_0"))

    tree_sensors = context.get_tree_sensors()
    # print(tree_sensors)

    wind_sensors = context.get_wind_sensors()
    # print(wind_sensors)

    try:
        context.create_fire_forest_status(
            "fire_forest_status_0",
            False,
            0.5,
            0.9,
            [(2, 1), (4, 3), (5, -1), (2, 1)]
        )
    except:
        pass

    print(context.get_entity("fire_forest_status_0"))

    context.delete_entity("fire_forest_status_0")

    print(context.find_device_by_serial("test"))
    print(context.find_devices_by_location((3,4), 10))

    for tree_sensor in tree_sensors:
        context.delete_entity(tree_sensor["id"])

    for wind_sensor in wind_sensors:
        context.delete_entity(wind_sensor["id"])

    subscriptions = context.list_subscriptions()
    # print(json.dumps(subscriptions, indent=4))

    for subscription in subscriptions:
        context.delete_subscription(subscription["id"])

from fastapi import FastAPI, Request
from pydantic import BaseModel

from datetime import datetime
from typing import Tuple, Dict, List

from context_broker import ContextBroker

app = FastAPI()
cb = ContextBroker("192.168.1.2")

class Tree(BaseModel):
    dateObserved: datetime
    id: str
    location: Tuple[float, float]
    co2: float|None
    humidity: float|None
    temperature: float|None

    @staticmethod
    def fromDict(data:Dict):
        return Tree(
            id=data["id"],
            dateObserved=data["dateObserved"],
            location=data["location"],
            co2=data["co2"],
            humidity=data["humidity"],
            temperature=data["temperature"]
        )

class Wind(BaseModel):
    dateObserved: datetime
    id: str
    location: Tuple[float, float]
    windDirection: float|None
    windSpeed: float|None

    @staticmethod
    def fromDict(data:Dict):
        return Wind(
            id=data["id"],
            dateObserved=data["dateObserved"],
            location=data["location"],
            windDirection=data["windDirection"],
            windSpeed=data["windSpeed"],
        )

class Co2(BaseModel):
    dateObserved: datetime
    id: str
    location: Tuple[float, float]
    co2: float|None

    @staticmethod
    def fromDict(data:Dict):
        return Co2(
            id=data["id"],
            dateObserved=data["dateObserved"],
            location=data["location"],
            co2=data["co2"],
        )

class Humidity(BaseModel):
    dateObserved: datetime
    id: str
    location: Tuple[float, float]
    humidity: float|None

    @staticmethod
    def fromDict(data:Dict):
        return Humidity(
            id=data["id"],
            dateObserved=data["dateObserved"],
            location=data["location"],
            humidity=data["humidity"],
        )

class Temperature(BaseModel):
    dateObserved: datetime
    id: str
    location: Tuple[float, float]
    temperature: float|None

    @staticmethod
    def fromDict(data:Dict):
        return Temperature(
            id=data["id"],
            dateObserved=data["dateObserved"],
            location=data["location"],
            temperature=data["temperature"],
        )

@app.get("/trees/{entity_id}")
@app.get("/wind/{entity_id}")
async def get_entity(entity_id) -> Tree|Wind:
    entity = cb.get_entity(entity_id)

    data = {
        "dateObserved": entity["dateObserved"],
        "id": entity_id,
        "location": entity["location"]["coordinates"],
    }

    entity_fields = entity["controlledProperty"]

    if entity["value"] is not None:
        tree_value = entity["value"].split("&")
    else:
        tree_value = [None for _ in range(len(entity_fields))]

    for i, field in enumerate(entity_fields):
        data[field] = tree_value[i]

    try:
        return Tree.fromDict(data)
    except:
        return Wind.fromDict(data)


@app.get("/temperature")
@app.get("/humidity")
@app.get("/co2")
async def get_tree_sensor_value(request: Request) -> List[Co2|Humidity|Temperature]:
    tree_sensors = cb.get_tree_sensors()

    data = []
    requestedValueName = request.url.path.lstrip('/')

    for tree_sensor in tree_sensors:
        try:
            values = tree_sensor["value"].split("&")
            index = tree_sensor["controlledProperty"].index(requestedValueName)
            requestedValue = values[index]
        except:
            requestedValue = None

        temp = {
            "dateObserved": tree_sensor["dateObserved"],
            "id": tree_sensor["id"],
            "location": tree_sensor["location"]["coordinates"],
            requestedValueName: requestedValue
        }

        match requestedValue:
            case "co2":
                temp = Co2.fromDict(temp)
            case "humidity":
                temp = Humidity.fromDict(temp)
            case "temperature":
                temp = Temperature.fromDict(temp)

        data.append(temp)

    return data

@app.get("/trees")
async def get_tree_sensor_values() -> List[Tree]:
    tree_sensors = cb.get_tree_sensors()

    trees = []

    for tree_sensor in tree_sensors:
        temp = {
            "dateObserved": tree_sensor["dateObserved"],
            "id": tree_sensor["id"],
            "location": tree_sensor["location"]["coordinates"],
            "co2": None,
            "humidity": None,
            "temperature": None,
        }
        try:
            values = tree_sensor["value"].split("&")

            for i, property in enumerate(tree_sensor["controlledProperty"]):
                temp[property] = values[i]
        except:
            pass

        trees.append(Tree.fromDict(temp))

    return trees

@app.get("/wind")
async def get_wind_values() -> List[Wind]:
    wind_sensors = cb.get_wind_sensors()

    wind = []

    for wind_sensor in wind_sensors:
        temp = {
            "dateObserved": wind_sensor["dateObserved"],
            "id": wind_sensor["id"],
            "location": wind_sensor["location"]["coordinates"],
            "windDirection": None,
            "windSpeed": None
        }
        try:
            values = wind_sensor["value"].split("&")
            for i, property in enumerate(wind_sensor["controlledProperty"]):
                temp[property] = values[i]
        except:
            pass

        wind.append(Wind.fromDict(temp))

    return wind

import uvicorn, sys, os

if __name__ == "__main__":

    reload = "--reload" in sys.argv

    file = os.path.basename(sys.argv[0]).rstrip('.py')

    uvicorn.run(f"{file}:app", host="0.0.0.0", port=3000, reload=reload)

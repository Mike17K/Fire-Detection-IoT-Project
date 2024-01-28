from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from datetime import datetime
from typing import Tuple, Dict, List

from context_broker import ContextBroker

app = FastAPI()
cb = ContextBroker("192.168.1.2")

origins = [
    "http://localhost:3000",
    "https://fireguard.mikekaipis.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


#### MODELS ####

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


#### UTILITY FUNCTIONS ####

def transform_entity(entity:Dict) -> Dict:

    data = {
        "dateObserved": entity["dateObserved"],
        "id": entity["id"],
        "location": entity["location"]["coordinates"],
    }

    entity_fields = entity["controlledProperty"]

    if entity["value"] is not None:
        tree_value = entity["value"].split("&")
    else:
        tree_value = [None for _ in range(len(entity_fields))]

    for i, field in enumerate(entity_fields):
        data[field] = tree_value[i]

    return data

def get_trees_attribute(attributeName:str) -> List[Dict]:
    tree_sensors = cb.get_tree_sensors()

    data = []

    for tree_sensor in tree_sensors:
        try:
            values = tree_sensor["value"].split("&")
            index = tree_sensor["controlledProperty"].index(attributeName)
            attribute = values[index]
        except:
            attribute = None

        temp = {
            "dateObserved": tree_sensor["dateObserved"],
            "id": tree_sensor["id"],
            "location": tree_sensor["location"]["coordinates"],
            attributeName: attribute
        }

        data.append(temp)

    return data


#### ROUTES ####

@app.get("/trees/{entity_id}")
async def get_tree(entity_id) -> Tree:
    entity = cb.get_entity(entity_id)
    return Tree.fromDict(transform_entity(entity))

@app.get("/wind/{entity_id}")
async def get_wind(entity_id) -> Wind:
    entity = cb.get_entity(entity_id)
    return Wind.fromDict(transform_entity(entity))


@app.get("/co2")
async def get_co2() -> List[Co2]:
    data = get_trees_attribute("co2")
    return list(map(Co2.fromDict, data))

@app.get("/humidity")
async def get_humidity() -> List[Humidity]:
    data = get_trees_attribute("humidity")
    return list(map(Humidity.fromDict, data))

@app.get("/temperature")
async def get_temperature() -> List[Temperature]:
    data = get_trees_attribute("temperature")
    return list(map(Temperature.fromDict, data))


@app.get("/trees")
async def get_tree_sensor_values() -> List[Tree]:
    tree_sensors = cb.get_tree_sensors()

    trees = []

    for tree_sensor in tree_sensors:
        trees.append(Tree.fromDict(transform_entity(tree_sensor)))

    return trees

@app.get("/wind")
async def get_wind_values() -> List[Wind]:
    wind_sensors = cb.get_wind_sensors()

    wind = []

    for wind_sensor in wind_sensors:
        wind.append(Wind.fromDict(transform_entity(wind_sensor)))

    return wind

import uvicorn, sys, os

if __name__ == "__main__":

    reload = "--reload" in sys.argv

    file = os.path.basename(sys.argv[0]).rstrip('.py')

    uvicorn.run(f"{file}:app", host="0.0.0.0", port=3000, reload=reload)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from datetime import datetime
from typing import Tuple, Dict, List

from context_broker import ContextBroker
from mysql_connection import DBConnection

from common_data import connection_host, lab_host

app = FastAPI()
cb = ContextBroker(connection_host)

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

class ForestStatus(BaseModel):
    dateObserved: datetime
    fireDetected: bool
    fireDetectedConfidence: float
    location: List[List[Tuple[float, float]]] | Tuple[float, float]

    @staticmethod
    def fromDict(data:Dict):
        return ForestStatus(
            dateObserved=data["dateObserved"],
            fireDetected=data["fireDetected"],
            fireDetectedConfidence=data["fireDetectedConfidence"],
            location=data["location"]["coordinates"]
        )


#### UTILITY FUNCTIONS ####

def reverse_entity_location(entity:Dict) -> Dict:
    # reverse coordinates from lon lat to the lat lon format for frontend use
    if entity["location"]["type"] == "Point":
        entity["location"]["coordinates"] = entity["location"]["coordinates"][::-1]

    elif entity["location"]["type"] == "Polygon":
        reversed_coords = []
        for segment in entity["location"]["coordinates"]:
            reversed_segment = []
            for point in segment:
                reversed_segment.append(point[::-1])
            reversed_coords.append(reversed_segment)
        entity["location"]["coordinates"] = reversed_coords

    return entity

def transform_device(entity:Dict) -> Dict:
    entity = reverse_entity_location(entity)

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
        tree_sensor = reverse_entity_location(tree_sensor)
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
def get_tree(entity_id) -> Tree:
    entity = cb.get_entity(entity_id)
    return Tree.fromDict(transform_device(entity))

@app.get("/wind/{entity_id}")
def get_wind(entity_id) -> Wind:
    entity = cb.get_entity(entity_id)
    return Wind.fromDict(transform_device(entity))


@app.get("/co2")
def get_co2() -> List[Co2]:
    data = get_trees_attribute("co2")
    return list(map(Co2.fromDict, data))

@app.get("/humidity")
def get_humidity() -> List[Humidity]:
    data = get_trees_attribute("humidity")
    return list(map(Humidity.fromDict, data))

@app.get("/temperature")
def get_temperature() -> List[Temperature]:
    data = get_trees_attribute("temperature")
    return list(map(Temperature.fromDict, data))


@app.get("/trees")
def get_tree_sensor_values() -> List[Tree]:
    tree_sensors = cb.get_tree_sensors()

    trees = []

    for tree_sensor in tree_sensors:
        trees.append(Tree.fromDict(transform_device(tree_sensor)))

    return trees

@app.get("/wind")
def get_wind_values() -> List[Wind]:
    wind_sensors = cb.get_wind_sensors()

    wind = []

    for wind_sensor in wind_sensors:
        wind.append(Wind.fromDict(transform_device(wind_sensor)))

    return wind

@app.get("/history/{entity_id}")
def get_history(entity_id) -> List[Dict]:
    db = DBConnection(lab_host)
    return db.get_history(entity_id)

@app.get("/forest_status")
def get_forest_status() -> ForestStatus:
    entity = cb.get_entity("forest_status_0")
    entity = reverse_entity_location(entity)
    return ForestStatus.fromDict(entity)

if __name__ == "__main__":
    import uvicorn, sys, os

    reload = "--reload" in sys.argv

    file = os.path.basename(sys.argv[0]).rstrip('.py')

    uvicorn.run(f"{file}:app", host="0.0.0.0", port=3000, reload=reload)

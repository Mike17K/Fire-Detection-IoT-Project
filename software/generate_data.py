import numpy as np
from uuid import uuid4
from datetime import datetime

from context_broker import ContextBroker

from typing import Dict, Tuple, Iterable, List

coord_limits = {
    "latitude": {
        "min": 38.28442,
        "max": 38.31899
    },
    "longitude": {
        "min": 21.88617,
        "max": 21.96498
    }
}

wind_coordinates = [
    (38.3006, 21.9362),
    (38.3138, 21.8767),
    (38.3014, 21.9070),
    (38.2790, 21.9248),
    (38.3127, 21.9374),
    (38.2967, 21.9620)
]

def generate_locations(
    coord_limits:Dict,
    grid_size:int
) -> Iterable[Tuple[float, float]]:

    latitudes = np.linspace(coord_limits["latitude"]["min"], coord_limits["latitude"]["max"], grid_size)
    longitudes = np.linspace(coord_limits["longitude"]["min"], coord_limits["longitude"]["max"], grid_size)

    for i in range(latitudes.size):
        for j in range(longitudes.size):
            location = (latitudes[i], longitudes[j])

            yield location

def generate_tree_sensors(
    broker_connection:ContextBroker,
    coord_limits:Dict,
    grid_size:int
) -> None:

    for i, location in enumerate(generate_locations(coord_limits, grid_size)):
        try:
            broker_connection.create_tree_sensor(f"tree_sensor_{i}", location, str(uuid4()))
            broker_connection.update_tree_sensor(
                f"tree_sensor_{i}",
                datetime.utcnow(),
                co2=i*2+1,
                humidity=i*3+2,
                temperature=i*5+3,
            )
        except Exception as e:
            print(e)

def generate_wind_sensors(
    broker_connection:ContextBroker,
    wind_coordinates:List[Tuple[float, float]],
) -> None:

    for i, location in enumerate(wind_coordinates):
        try:
            broker_connection.create_wind_sensor(f"wind_sensor_{i}", location, str(uuid4()))
            broker_connection.update_wind_sensor(
                f"wind_sensor_{i}",
                datetime.utcnow(),
                windDirection=(i*5+1)%360,
                windSpeed=i*3+2,
            )
        except Exception as e:
            print(e)



if __name__ == "__main__":
    cb = ContextBroker("192.168.1.2")

    tree_grid_size = 10
    generate_tree_sensors(cb, coord_limits, tree_grid_size)

    generate_wind_sensors(cb, wind_coordinates)

    print(cb.get_tree_sensors())
    print(cb.get_wind_sensors())

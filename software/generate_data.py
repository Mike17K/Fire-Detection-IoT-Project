import numpy as np
from uuid import uuid4

from context_broker import ContextBroker

from typing import Dict, Tuple, Iterable

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
        broker_connection.create_tree_sensor(f"tree_sensor_{i}", location, str(uuid4()))


if __name__ == "__main__":
    cb = ContextBroker("192.168.1.2")

    grid_size = 10
    generate_tree_sensors(cb, coord_limits, grid_size)

    for i in range(grid_size ** 2):
        print(cb.get_entity(f"tree_sensor_{i}"))

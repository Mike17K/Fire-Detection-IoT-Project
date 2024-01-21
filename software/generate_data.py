from uuid import uuid4
from datetime import datetime

from shapely.geometry import Polygon
from pointpats import random as rng

from context_broker import ContextBroker

from typing import Tuple, List

trees_polygon = [
    (38.27095,21.92257),
    (38.29897,21.98112),
    (38.31716,21.95278),
    (38.31635,21.91518),
    (38.30934,21.86109),
    (38.28941,21.88135)
]

trees_polygon = Polygon([coord[::-1] for coord in trees_polygon])

wind_coordinates = [
    (38.3006, 21.9362),
    (38.3138, 21.8767),
    (38.3014, 21.9070),
    (38.2790, 21.9248),
    (38.3127, 21.9374),
    (38.2967, 21.9620)
]

def generate_tree_sensors(
    broker_connection:ContextBroker,
    polygon:Polygon,
    num_of_sensors:int
) -> None:

    coords = rng.cluster_poisson(polygon, size=num_of_sensors, n_seeds=num_of_sensors//5, cluster_radius=0.1)
    coords = coords.tolist()

    for i, location in enumerate(coords):
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

    generate_tree_sensors(cb, trees_polygon, 200)

    generate_wind_sensors(cb, wind_coordinates)

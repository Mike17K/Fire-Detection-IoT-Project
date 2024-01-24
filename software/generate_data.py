from uuid import uuid4
from datetime import datetime

from shapely.geometry import Polygon, Point
from shapely.prepared import prep

import numpy as np

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

def gen_points_in_polygon(
    polygon:Polygon,
    num_of_points:int
) -> List[Tuple[float, float]]:

    min_x, min_y, max_x, max_y = polygon.bounds

    spacing = int(num_of_points ** 0.5)

    points = []
    while len(points) < num_of_points:
        x_spacing = (max_x - min_x) / spacing
        y_spacing = (max_y - min_y) / spacing

        x = np.arange(np.floor(min_x), int(np.ceil(max_x)), x_spacing)
        y = np.arange(np.floor(min_y), int(np.ceil(max_y)), y_spacing)

        xx, yy = np.meshgrid(x,y)

        pts = [Point(X,Y) for X,Y in zip(xx.ravel(),yy.ravel())]

        points = list(filter(prep(polygon).contains, pts))

        spacing += 1

    return [(point.x, point.y) for point in points]

def generate_tree_sensors(
    broker_connection:ContextBroker,
    polygon:Polygon,
    num_of_sensors:int
) -> None:

    coords = gen_points_in_polygon(polygon, num_of_sensors)

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

    generate_tree_sensors(cb, trees_polygon, 150)

    generate_wind_sensors(cb, wind_coordinates)

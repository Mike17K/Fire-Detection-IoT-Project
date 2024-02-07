from uuid import uuid4
from datetime import datetime, timedelta, timezone
import asyncio, random

from shapely.geometry import Polygon, Point
from shapely.prepared import prep

import numpy as np

from perlin_noise import PerlinNoise

from context_broker import ContextBroker

trees_polygon = [
    (38.27095,21.92257),
    (38.29897,21.98112),
    (38.31716,21.95278),
    (38.31635,21.91518),
    (38.30934,21.86109),
    (38.28941,21.88135)
]

trees_polygon = Polygon([coord[::-1] for coord in trees_polygon])

wind_coordinates = [(coord[1], coord[0]) for coord in [
    (38.30063, 21.93641),
    (38.31386, 21.87669),
    (38.30138, 21.90701),
    (38.27893, 21.92458),
    (38.31069, 21.93780),
    (38.29677, 21.96190)
]]

co2_stats = {
    "mean": 380,
    "deviation": 20,
}

humidity_stats = {
    "mean": 50,
    "deviation": 10,
}

temperature_stats = {
    "mean": 20,
    "deviation": 5,
}

wind_direction_stats = {
    "mean": 15,
    "deviation": 2,
}

wind_speed_stats = {
    "mean": 15,
    "deviation": 2,
}

def gen_points_in_polygon(
    polygon:Polygon,
    num_of_points:int
) -> list[tuple[float, float]]:

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
        except Exception as e:
            print(e)

def generate_wind_sensors(
    broker_connection:ContextBroker,
    wind_coordinates:list[tuple[float, float]],
) -> None:

    for i, location in enumerate(wind_coordinates):
        try:
            broker_connection.create_wind_sensor(f"wind_sensor_{i}", location, str(uuid4()))
        except Exception as e:
            print(e)

async def steady_state_tree_values(
    broker_connection:ContextBroker,
    co2_stats:dict,
    humidity_stats:dict,
    temperature_stats:dict,
    update_cycles:int = 1
) -> None:

    seed = 0
    for _ in range(update_cycles):
        seed += 1

        co2_noise = PerlinNoise(octaves=1, seed=2*seed)
        humidity_noise = PerlinNoise(octaves=1, seed=3*seed)
        temperature_noise = PerlinNoise(octaves=1, seed=5*seed)

        trees = broker_connection.get_tree_sensors()
        random.shuffle(trees)

        for tree in trees:
            tree_location = tree["location"]["coordinates"]

            tree_co2 = co2_stats["mean"] + co2_noise(tree_location) * co2_stats["deviation"]
            tree_co2 = float(f"{tree_co2:.2f}")

            tree_humidity = humidity_stats["mean"] + humidity_noise(tree_location) * humidity_stats["deviation"]
            tree_humidity = float(f"{tree_humidity:.2f}")

            tree_temp = temperature_stats["mean"] + temperature_noise(tree_location) * temperature_stats["deviation"]
            tree_temp = float(f"{tree_temp:.2f}")

            print(tree["id"], tree_co2, tree_humidity, tree_temp)

            broker_connection.update_tree_sensor(tree["id"], dateObserved=datetime.utcnow(), co2=tree_co2, humidity=tree_humidity, temperature=tree_temp)

            await asyncio.sleep(10/len(trees))

async def steady_state_wind_values(
    broker_connection:ContextBroker,
    wind_direction_stats:dict,
    wind_speed_stats:dict,
    update_cycles:int = 1
) -> None:

    seed = 0
    for _ in range(update_cycles):
        seed += 1

        wind_direction_noise = PerlinNoise(octaves=1, seed=2*seed)
        wind_speed_noise = PerlinNoise(octaves=1, seed=3*seed)

        wind_sensors = broker_connection.get_wind_sensors()
        random.shuffle(wind_sensors)

        for wind in wind_sensors:
            wind_location = wind["location"]["coordinates"]

            wind_direction = wind_direction_stats["mean"] + wind_direction_noise(wind_location) * wind_direction_stats["deviation"]
            wind_direction = int(wind_direction)

            wind_speed = wind_speed_stats["mean"] + wind_speed_noise(wind_location) * wind_speed_stats["deviation"]
            wind_speed = float(f"{wind_speed:.2f}")

            print(wind["id"], wind_direction, wind_speed)

            broker_connection.update_wind_sensor(wind["id"], dateObserved=datetime.utcnow(), windDirection=wind_direction, windSpeed=wind_speed)

            await asyncio.sleep(10/len(wind_sensors))

async def main():
    random.seed(0)

    cb = ContextBroker("192.168.1.2")

    generate_tree_sensors(cb, trees_polygon, 150)
    generate_wind_sensors(cb, wind_coordinates)

    async with asyncio.TaskGroup() as tg:
        trees_task = tg.create_task(steady_state_tree_values(cb, co2_stats, humidity_stats, temperature_stats))
        wind_task = tg.create_task(steady_state_wind_values(cb, wind_direction_stats, wind_speed_stats))

if __name__ == "__main__":
    asyncio.run(main())

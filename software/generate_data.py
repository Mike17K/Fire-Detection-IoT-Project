from uuid import uuid4
from datetime import datetime, timedelta, timezone
import asyncio, random

from shapely.geometry import Polygon, Point
from shapely.prepared import prep

from geopy import distance

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

trees_polygon = Polygon([coord[::-1] for coord in trees_polygon]) # lon lat

wind_coordinates = [(coord[1], coord[0]) for coord in [
    (38.30063, 21.93641),
    (38.31386, 21.87669),
    (38.30138, 21.90701),
    (38.27893, 21.92458),
    (38.31069, 21.93780),
    (38.29677, 21.96190)
]] # lon lat

steady_state_tree_stats = {
    "co2": { # ppm
        "mean": 380,
        "deviation": 20,
    },
    "humidity": { # %RH
        "mean": 50,
        "deviation": 10,
    },
    "temperature": { # degrees C
        "mean": 20,
        "deviation": 5,
    }
}

steady_state_wind_stats = {
    "wind_direction": { # compass heading
        "mean": 270,
        "deviation": 2,
    },
    "wind_speed": { # m/s
        "mean": 9,
        "deviation": 1,
    }
}

fire_stats = {
    "center": (38.30337,21.91896), # lat, lon
    "radius": 1246, # m
    "co2": { # ppm
        "mean": 1000,
        "deviation": 80
    },
    "humidity": { # %RH
        "mean": 5,
        "deviation": 2
    },
    "temperature": { # degrees C
        "mean": 80,
        "deviation": 20
    },
}


#### GENERATE DEVICES ####
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


#### GENERATE TREE VALUES ####
async def steady_state_tree_values(
    broker_connection:ContextBroker,
    tree_sensor:dict,
    co2_stats:dict,
    humidity_stats:dict,
    temperature_stats:dict,
    seed:int = 1
) -> None:

    co2_noise = PerlinNoise(octaves=1, seed=2*seed)
    humidity_noise = PerlinNoise(octaves=1, seed=3*seed)
    temperature_noise = PerlinNoise(octaves=1, seed=5*seed)

    tree_location = tree_sensor["location"]["coordinates"]

    tree_co2 = co2_stats["mean"] + co2_noise(tree_location) * co2_stats["deviation"]
    tree_co2 = float(f"{tree_co2:.2f}")

    tree_humidity = humidity_stats["mean"] + humidity_noise(tree_location) * humidity_stats["deviation"]
    tree_humidity = float(f"{tree_humidity:.2f}")

    tree_temp = temperature_stats["mean"] + temperature_noise(tree_location) * temperature_stats["deviation"]
    tree_temp = float(f"{tree_temp:.2f}")

    print(tree_sensor["id"], tree_co2, tree_humidity, tree_temp)

    broker_connection.update_tree_sensor(
        tree_sensor["id"],
        dateObserved=datetime.utcnow(),
        co2=tree_co2,
        humidity=tree_humidity,
        temperature=tree_temp
    )

async def fire_tree_values(
    broker_connection:ContextBroker,
    tree_sensor:dict,
    co2_stats:dict,
    humidity_stats:dict,
    temperature_stats:dict,
    seed:int
) -> None:

    co2_noise = PerlinNoise(octaves=1, seed=2*seed)
    humidity_noise = PerlinNoise(octaves=1, seed=3*seed)
    temperature_noise = PerlinNoise(octaves=1, seed=5*seed)

    tree_location = tree_sensor["location"]["coordinates"]

    tree_co2 = co2_stats["mean"] + co2_noise(tree_location) * co2_stats["deviation"]
    tree_co2 = float(f"{tree_co2:.2f}")

    tree_humidity = humidity_stats["mean"] + humidity_noise(tree_location) * humidity_stats["deviation"]
    tree_humidity = float(f"{tree_humidity:.2f}")

    tree_temp = temperature_stats["mean"] + temperature_noise(tree_location) * temperature_stats["deviation"]
    tree_temp = float(f"{tree_temp:.2f}")

    print(tree_sensor["id"], tree_co2, tree_humidity, tree_temp)

    broker_connection.update_tree_sensor(
        tree_sensor["id"],
        dateObserved=datetime.utcnow(),
        co2=tree_co2,
        humidity=tree_humidity,
        temperature=tree_temp
    )

async def generate_tree_values(
    broker_connection:ContextBroker,
    steady_state_tree_stats:dict,
    fire_stats:dict,
    update_cycles:int = 1
) -> None:

    for seed in range(update_cycles):

        fire_radius_noise = PerlinNoise(octaves=20, seed=2*seed)

        tree_sensors = broker_connection.get_tree_sensors()
        random.shuffle(tree_sensors)

        for tree_sensor in tree_sensors:
            tree_sensor_location = tree_sensor["location"]["coordinates"][::-1]

            distance_to_fire_center = distance.distance(fire_stats["center"], tree_sensor_location).m
            distance_variation = fire_radius_noise(tree_sensor_location)

            if distance_to_fire_center < fire_stats["radius"] * seed/update_cycles * (1 + distance_variation/10):
                await fire_tree_values(
                    broker_connection,
                    tree_sensor,
                    fire_stats["co2"],
                    fire_stats["humidity"],
                    fire_stats["temperature"],
                    seed
                )
            else:
                await steady_state_tree_values(
                    broker_connection,
                    tree_sensor,
                    steady_state_tree_stats["co2"],
                    steady_state_tree_stats["humidity"],
                    steady_state_tree_stats["temperature"],
                    seed+1
                )

            await asyncio.sleep(10/len(tree_sensors))


#### GENERATE WIND VALUES ####
async def steady_state_wind_values(
    broker_connection:ContextBroker,
    wind_sensor:dict,
    wind_direction_stats:dict,
    wind_speed_stats:dict,
    seed:int
) -> None:

    wind_direction_noise = PerlinNoise(octaves=1, seed=2*seed)
    wind_speed_noise = PerlinNoise(octaves=1, seed=3*seed)

    wind_location = wind_sensor["location"]["coordinates"]

    wind_direction = wind_direction_stats["mean"] + wind_direction_noise(wind_location) * wind_direction_stats["deviation"]
    wind_direction = int(wind_direction)

    wind_speed = wind_speed_stats["mean"] + wind_speed_noise(wind_location) * wind_speed_stats["deviation"]
    wind_speed = float(f"{wind_speed:.2f}")

    print(wind_sensor["id"], wind_direction, wind_speed)

    broker_connection.update_wind_sensor(
        wind_sensor["id"],
        dateObserved=datetime.utcnow(),
        windDirection=wind_direction,
        windSpeed=wind_speed
    )

async def generate_wind_values(
    broker_connection:ContextBroker,
    steady_state_wind_stats:dict,
    update_cycles:int = 1
) -> None:

    for seed in range(update_cycles):

        wind_sensors = broker_connection.get_wind_sensors()
        random.shuffle(wind_sensors)

        for wind_sensor in wind_sensors:

            await steady_state_wind_values(
                broker_connection,
                wind_sensor,
                steady_state_wind_stats["wind_direction"],
                steady_state_wind_stats["wind_speed"],
                seed+1
            )

            await asyncio.sleep(10/len(wind_sensors))


async def main():
    random.seed(0)

    cb = ContextBroker("192.168.1.2")

    generate_tree_sensors(cb, trees_polygon, 150)
    generate_wind_sensors(cb, wind_coordinates)

    update_cycles = 10

    async with asyncio.TaskGroup() as tg:
        trees_task = tg.create_task(generate_tree_values(cb, steady_state_tree_stats, fire_stats, update_cycles))
        wind_task = tg.create_task(generate_wind_values(cb, steady_state_wind_stats, update_cycles))

if __name__ == "__main__":
    asyncio.run(main())

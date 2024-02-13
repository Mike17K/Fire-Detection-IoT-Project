from ai.model.predict import predict
import numpy as np
import time

from context_broker import ContextBroker
from public_api import get_tree_sensor_values
from generate_data import trees_polygon_coords

cb = ContextBroker("150.140.186.118")

def preprocess_data(data:list[dict]) -> list:
  tmp_data = []
  min_val = [0,0,0] # temp, hum, co2
  max_val = [100,100,800] # temp, hum, co2
  for d in data:
      temp_data = (d['temperature'] - min_val[0]) / (max_val[0] - min_val[0])
      hum_data = (d['humidity'] - min_val[1]) / (max_val[1] - min_val[1])
      co2_data = (d['co2'] - min_val[2]) / (max_val[2] - min_val[2])
      tmp_data += [temp_data, hum_data, co2_data]
  return tmp_data

def fire_detection() -> None:
  cb.create_fire_forest_status(
    "forest_status_0",
    False,
    1,
    0,
    trees_polygon_coords
  )

  tree_sensors = [dict(device) for device in get_tree_sensor_values()]

  sensor_data = np.array([
    preprocess_data(tree_sensors)
  ])

  prediction = predict(sensor_data) # returns the probability of fire
  print(prediction)

  fire = True if prediction > 0.5 else False

  cb.update_fire_forest_status(
    "forest_status_0",
    fire,
    prediction[0],
    0,
  )

if __name__ == "__main__":
  fire_detection()

  time.sleep(10)

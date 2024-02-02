from model import predict
import numpy as np

# Test Data

# Steps 
# 1. Fetch data
# 2. Normalize data
# 3. Call model and get predictions
# 4. Compare predictions to a threshold

# data from 150 sensors: 150 values temperature, 150 values humidity, 150 values co2
# data limits: temperature: 0-1000, humidity: 0-100, co2: 0-800

# Test 1: ( Normal Data: 450 values )
sensor_data = np.array([
  # ???
])

print(predict(sensor_data))

# new sensor data 
# compare to threshold
# fetch the around sensors 
# pass to the predict 
# 

# s: position 
# fire center: position
# tmp: 200/ (0.0001*r)

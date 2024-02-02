from model import predict
import numpy as np

# Test Data

# Steps 
# 1. Fetch data
# 2. Normalize data
# 3. Call model and get predictions
# 4. Compare predictions to a threshold

# data from 10 sensors: 10 values temperature, 10 values humidity, 10 values co2
# data limits: temperature: 0-200, humidity: 0-100, co2: 0-500

# Test 1
sensor_data = np.array([
  [100,50,40,20,50,50,70,40,40,40,10,5,1,10,10,20,20,10,1,10,400,400,400,400,400,400,400,400,400,300],
  [25,25,25,25,25,25,25,25,25,25,30,30,30,30,30,30,30,30,30,30,200,200,200,200,200,200,200,200,200,200],
])

print(predict(sensor_data))

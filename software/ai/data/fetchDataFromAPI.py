import requests
import numpy as np

N = 10
min_val = [0,0,0] # temp, hum, co2
max_val = [1000,100,800] # temp, hum, co2

data = []
for i in range(N):
    r = requests.get('https://iot.alkalyss.gr/trees', auth=('user', 'pass'))
    if r.status_code == 200:
        allSensorData = r.json()
        print(i + 1," : Data fetched successfully!", len(allSensorData))
        tmp_data = []
        for sensorData in allSensorData:
            temp_normalized = (sensorData['temperature'] - min_val[0]) / (max_val[0] - min_val[0])
            hum_normalized = (sensorData['humidity'] - min_val[1]) / (max_val[1] - min_val[1])
            co2_normalized = (sensorData['co2'] - min_val[2]) / (max_val[2] - min_val[2])
            tmp_data += [temp_normalized, hum_normalized, co2_normalized]
        data.append(tmp_data)


# Path: software/ai/data/produceData.py
filepath = "\\".join(__file__.split("\\")[:-1])+f"\\normal_data_from_api.csv"
# write data to file
np.savetxt(filepath, data, delimiter=",")

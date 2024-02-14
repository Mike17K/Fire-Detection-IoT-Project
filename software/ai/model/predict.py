from .model import AnomalyDetector
import numpy as np

import os

autoencoder = None

def init():
  """
    Initializes the model
  """
  global autoencoder
  if autoencoder is not None: return
  autoencoder = AnomalyDetector()
  autoencoder.compile(optimizer='adam', loss='mae')

  # load saved model if available
  
  script_dir = os.path.dirname(os.path.realpath(__file__))

  try:
    path = os.path.join(script_dir, "cache")
    print(path)
    autoencoder.load(path, filenameStartsWith="autoencoder")
    print("Model found, loading it")
  except Exception as e:
    print(e)
    print("No model found, using a new one")

def normalizeSensorData(data: np.ndarray):
  """
    Normalizes the data to [0,1].
    data: a numpy array of shape (n, 450), 150 sensors with 3 values each, ( temperature, humidity, co2 )
  """
  init()
  assert data.shape[1] == 450, "Data should have 450 columns"

  min_val = [0,0,0] # temp, hum, co2
  max_val = [100,100,800] # temp, hum, co2
  for i in range(data.shape[1]):
      data[:,i] = (data[:,i] - min_val[(i)%3]) / (max_val[(i)%3] - min_val[(i)%3])
  return data

def predict(data: np.ndarray) -> np.ndarray:
  """
    Predicts the anomaly score for a given data point
    data: a tensor of shape (n, 450), 150 sensors with 3 values each, ( temperature, humidity, co2 )
    returns: an array of shape (n, ) with the anomaly score for each data point
  """
  global autoencoder
  init()
  assert data.shape[1] == 450, "Data should have 450 columns"

  data = normalizeSensorData(data)
  predictions = autoencoder.call(data)
  output = np.max(np.abs(predictions - data), axis=1)  
  # print(output)
  # anomalus output variable : 0.52053255 
  # normal output variable : 0.5205132
  estimation = ( output - 0.5205132 ) / (0.52053255 - 0.5205132)
  # clip the estimation to [0,1]
  estimation = np.clip(estimation, 0, 1)
  estimation_propability = np.exp(5*(estimation-0.5)) / (1 + np.exp(5*(estimation-0.5)))
  return estimation_propability

from .model import AnomalyDetector
import numpy as np

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
  try:
    autoencoder.load("\\".join(__file__.split("\\")[:-1])+f"\\cache\\autoencoder")
    print("Model found, loading it")
  except:
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
  return np.max(np.abs(predictions - data), axis=1)

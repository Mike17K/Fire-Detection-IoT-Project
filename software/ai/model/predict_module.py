import numpy as np
import tensorflow as tf

class AnomalyDetector(tf.keras.models.Model):
  def __init__(self):
    super(AnomalyDetector, self).__init__()
    self.encoder = tf.keras.Sequential([
      tf.keras.layers.Dense(30, activation="relu"), # 30 = 10 sensors * 3 values
      tf.keras.layers.Dense(16, activation="relu"),
      tf.keras.layers.Dense(8, activation="relu")])

    self.decoder = tf.keras.Sequential([
      tf.keras.layers.Dense(16, activation="relu"),
      tf.keras.layers.Dense(30, activation="sigmoid")]) # 30 = 10 sensors * 3 values
  
  def save(self, path):
    self.encoder.save(path + "_encoder.keras")
    self.decoder.save(path + "_decoder.keras")
  
  def load(self, path):
    self.encoder = tf.keras.models.load_model(path + "_encoder.keras")
    self.decoder = tf.keras.models.load_model(path + "_decoder.keras")

  def call(self, x):
    encoded = self.encoder(x)
    decoded = self.decoder(encoded)
    return decoded

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
    data: a numpy array of shape (n, 30), 10 sensors with 3 values each, ( temperature, humidity, co2 )
  """
  min_val = [0,0,0] # temp, hum, co2
  max_val = [200,100,500] # temp, hum, co2
  for i in range(data.shape[1]):
      data[:,i] = (data[:,i] - min_val[(i)%3]) / (max_val[(i)%3] - min_val[(i)%3])
  return data

def predict(data: np.ndarray) -> np.ndarray:
  """
    Predicts the anomaly score for a given data point
    data: a tensor of shape (n, 30), 10 sensors with 3 values each, ( temperature, humidity, co2 )
    returns: an array of shape (n, ) with the anomaly score for each data point
  """
  data = normalizeSensorData(data)
  predictions = autoencoder.call(data)
  return np.mean(np.abs(predictions - data), axis=1)

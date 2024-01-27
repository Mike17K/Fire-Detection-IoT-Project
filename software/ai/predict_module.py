from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, losses
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Model

class AnomalyDetector(Model):
  def __init__(self):
    super(AnomalyDetector, self).__init__()
    self.encoder = tf.keras.Sequential([
      layers.Dense(30, activation="relu"), # 30 = 10 sensors * 3 values
      layers.Dense(16, activation="relu"),
      layers.Dense(8, activation="relu")])

    self.decoder = tf.keras.Sequential([
      layers.Dense(16, activation="relu"),
      layers.Dense(30, activation="sigmoid")]) # 30 = 10 sensors * 3 values
  
  def save(self, path):
    self.encoder.save(path + "_encoder.h5")
    self.decoder.save(path + "_decoder.h5")
  
  def load(self, path):
    self.encoder = tf.keras.models.load_model(path + "_encoder.h5")
    self.decoder = tf.keras.models.load_model(path + "_decoder.h5")

  def call(self, x):
    encoded = self.encoder(x)
    decoded = self.decoder(encoded)
    return decoded

autoencoder = AnomalyDetector()
autoencoder.compile(optimizer='adam', loss='mae')

# load saved model if available
try:
  autoencoder.load("\\".join(__file__.split("\\")[:-1])+f"\\model\\autoencoder")
  print("Model found, loading it")
except:
  print("No model found, creating a new one")


# make predictions
def predict(data: tf.Tensor) -> np.ndarray:
  """
    Predicts the anomaly score for a given data point
    data: a tensor of shape (n, 30), 10 sensors with 3 normalized values each, ( temperature, humidity, co2 )
    returns: an array of shape (n, ) with the anomaly score for each data point
  """
  predictions = autoencoder.call(data)
  return np.mean(np.abs(predictions - data), axis=1)

# test data with anomalies
# data = tf.random.normal([1, 30])
# print(data)
# print(predict(data))

# Steps 
# 1. Fetch data
# 2. Normalize data
# 3. Call model and get predictions
# 4. Compare predictions to a threshold
import tensorflow as tf
import os

class AnomalyDetector(tf.keras.models.Model):
  def __init__(self):
    super(AnomalyDetector, self).__init__()
    self.encoder = tf.keras.Sequential([
      tf.keras.layers.Dense(450, activation="relu"), # 450 = 150 sensors * 3 values
      tf.keras.layers.Dense(32, activation="relu"),
      tf.keras.layers.Dense(16, activation="relu")])


    self.decoder = tf.keras.Sequential([
      tf.keras.layers.Dense(16, activation="relu"),
      tf.keras.layers.Dense(32, activation="relu"),
      tf.keras.layers.Dense(450, activation="sigmoid")]) # 450 = 150 sensors * 3 values

  def load(self, path, filenameStartsWith="autoencoder"):
    encoderFilePath = os.path.join(path, filenameStartsWith + "_encoder.tf")
    decoderFilePath = os.path.join(path, filenameStartsWith + "_decoder.tf")

    self.encoder = tf.keras.models.load_model(encoderFilePath)
    self.decoder = tf.keras.models.load_model(decoderFilePath)
  
  def save(self, path, filenameStartsWith="autoencoder"):
    self.encoder.save(os.path.join(path, filenameStartsWith + "_encoder.tf"))
    self.decoder.save(os.path.join(path, filenameStartsWith + "_decoder.tf"))

  def call(self, x):
    encoded = self.encoder(x)
    decoded = self.decoder(encoded)
    return decoded

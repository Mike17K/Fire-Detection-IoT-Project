import tensorflow as tf

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

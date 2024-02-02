from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, losses
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Model

# load from csv
dataframe = pd.read_csv("\\".join(__file__.split("\\")[:-2])+f"\\data\\data.csv", header=None)

SAMPLES_SIZE = dataframe.shape[0]

# The first element contains the labels
labels = dataframe.values[:, 0].astype(bool)

data = dataframe.values[:, 1:]

test_data = data[int(0.8*SAMPLES_SIZE):,:]
test_labels = labels[int(0.8*SAMPLES_SIZE):]
train_data = data[:int(0.8*SAMPLES_SIZE),:]
train_labels = labels[:int(0.8*SAMPLES_SIZE)]


# Plot a normal ECG.
N = 200
N = min(N, SAMPLES_SIZE)

print("Train data shape: ", train_data.shape)
print("Train labels shape: ", train_labels.shape)
print("Test data shape: ", test_data.shape)
print("Test labels shape: ", test_labels.shape)

# get only training data that is normal
normal_train_data = []
anomalous_train_data = []
for i in range(len(train_labels)):
    if train_labels[i] == False:
        normal_train_data.append(train_data[i])
    else:
        anomalous_train_data.append(train_data[i])
normal_train_data = np.array(normal_train_data)
anomalous_train_data = np.array(anomalous_train_data)

# Plot a normal ECG.
N = 200
N = min(N, len(normal_train_data))

# plt.grid()
# plt.plot(np.arange(N), normal_train_data[:N,0], color='red')
# plt.plot(np.arange(N), normal_train_data[:N,1], color='blue')
# plt.plot(np.arange(N), normal_train_data[:N,2], color='green')
# plt.title("A Normal ECG")
# plt.show()


# Build the model

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
  print("No model found, creating a new one")


# Train the model
history = autoencoder.fit(normal_train_data, normal_train_data, 
          epochs=20, 
          batch_size=512,
          validation_data=(test_data, test_data),
          shuffle=True)

# save model to file
autoencoder.save("\\".join(__file__.split("\\")[:-1])+f"\\cache\\autoencoder")

plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.legend()
plt.show()

# Detect anomalies
# Get train MAE loss.
train_loss = autoencoder.evaluate(normal_train_data, normal_train_data)
print("Train loss: ", train_loss)

# Get test MAE loss.
test_loss = autoencoder.evaluate(test_data, test_data)
print("Test loss: ", test_loss)


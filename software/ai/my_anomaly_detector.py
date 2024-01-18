from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, losses
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Model

# TODO build better data from simulation

def smooth_random_changes_2d(shape, smoothness):
    # Create smooth noise
    noise = np.random.uniform(-1, 1, size=shape)
    noise = np.clip(noise, -1, 1)
    noise[0, :] = 0
    noise[-1, :] = 0
    noise[:, 0] = 0
    noise[:, -1] = 0

    # Smooth noise
    for i in range(1, shape[0]-1):
        for j in range(1, shape[1]-1):
            noise[i, j] = (noise[i-1, j-1] + noise[i-1, j] + noise[i-1, j+1] +
                           noise[i, j-1] + noise[i, j] + noise[i, j+1] +
                           noise[i+1, j-1] + noise[i+1, j] + noise[i+1, j+1]) / 9

    # Scale smooth noise
    noise = noise / np.max(np.abs(noise))

    # Add smooth noise to the data
    return smoothness * noise

SAMPLES_SIZE = 1000
NUMBER_OF_SENSORS = 10

# Create Normal Dataset Dummy
temperatures_normal = 20+5*smooth_random_changes_2d((SAMPLES_SIZE, NUMBER_OF_SENSORS), 0.1)
humidity_normal = 100+50*smooth_random_changes_2d((SAMPLES_SIZE, NUMBER_OF_SENSORS), 0.1)
co2_normal = 250+20*smooth_random_changes_2d((SAMPLES_SIZE, NUMBER_OF_SENSORS), 0.1 )

data_normal = np.concatenate((temperatures_normal, humidity_normal, co2_normal), axis=1)

labels_normal = np.zeros((SAMPLES_SIZE, 1))

# Create Anomalous Dataset Dummy
temperatures_anomalous = 40+23*smooth_random_changes_2d((SAMPLES_SIZE, NUMBER_OF_SENSORS), 0.1)
humidity_anomalous = 20+10*smooth_random_changes_2d((SAMPLES_SIZE, NUMBER_OF_SENSORS), 0.1)
co2_anomalous = 400+100*smooth_random_changes_2d((SAMPLES_SIZE, NUMBER_OF_SENSORS), 0.1)

data_anomalous = np.concatenate((temperatures_anomalous, humidity_anomalous, co2_anomalous), axis=1)

labels_anomalous = np.ones((SAMPLES_SIZE, 1))

# Concatenate the normal and anomalous observations
data = np.concatenate((data_normal, data_anomalous), axis=0)
labels = np.concatenate((labels_normal, labels_anomalous), axis=0)

# Normalize the data to [0,1].
min_temp = np.min(data[:,0]) # this is the temperature
max_temp = np.max(data[:,0])

data[:,0] = (data[:,0] - min_temp) / (max_temp - min_temp)

min_hum = np.min(data[:,1]) # this is the humidity
max_hum = np.max(data[:,1])

data[:,1] = (data[:,1] - min_hum) / (max_hum - min_hum)

min_co2 = np.min(data[:,2]) # this is the co2
max_co2 = np.max(data[:,2])

data[:,2] = (data[:,2] - min_co2) / (max_co2 - min_co2)

# You will train the autoencoder using only the normal rhythms, which are labeled in this dataset as 1. Separate the normal rhythms from the abnormal rhythms.
labels = labels.astype(bool)

test_data = data[int(0.8*SAMPLES_SIZE):,:]
test_labels = labels[int(0.8*SAMPLES_SIZE):]
train_data = data[:int(0.8*SAMPLES_SIZE),:]
train_labels = labels[:int(0.8*SAMPLES_SIZE)]


# Plot a normal ECG.
N = 200
N = min(N, SAMPLES_SIZE)

# plt.grid()
# plt.plot(np.arange(N), data_normal[:N,0], color='red')
# plt.plot(np.arange(N), data_normal[:N,1], color='blue')
# plt.plot(np.arange(N), data_normal[:N,2], color='green')
# plt.title("A Normal ECG")
# plt.show()

# # Plot an anomalous ECG.

# plt.grid()
# plt.plot(np.arange(N), data_anomalous[:N,0], color='red')
# plt.plot(np.arange(N), data_anomalous[:N,1], color='blue')
# plt.plot(np.arange(N), data_anomalous[:N,2], color='green')
# plt.title("An Anomalous ECG")
# plt.show()

print("Train data shape: ", train_data.shape)
print("Train labels shape: ", train_labels.shape)
print("Test data shape: ", test_data.shape)
print("Test labels shape: ", test_labels.shape)

# get only training data that is normal
normal_train_data = []
anomalous_train_data = []
for i in range(len(train_labels)):
    if train_labels[i][0] == False:
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

  def call(self, x):
    encoded = self.encoder(x)
    decoded = self.decoder(encoded)
    return decoded

autoencoder = AnomalyDetector()
autoencoder.compile(optimizer='adam', loss='mae')

# Train the model
history = autoencoder.fit(normal_train_data, normal_train_data, 
          epochs=20, 
          batch_size=512,
          validation_data=(normal_train_data, normal_train_data),
          shuffle=True)

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

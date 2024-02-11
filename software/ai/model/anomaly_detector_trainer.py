from model import AnomalyDetector
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

if __name__ == "__main__":
  # load from csv
  dataframe = pd.read_csv("\\".join(__file__.split("\\")[:-2])+f"\\data\\normal_data_from_api.csv", header=None)
  datasetHasLabels = dataframe.shape[1] % 2 == 1
  if not datasetHasLabels:
    # add all False in the first column
      dataframe.insert(0, 'label', False)

  anomalus_data = pd.read_csv("\\".join(__file__.split("\\")[:-2])+f"\\data\\anomalus_data_from_api.csv", header=None).astype(np.float32)


  SAMPLES_SIZE = dataframe.shape[0]

  # The first element contains the labels
  labels = dataframe.values[:, 0].astype(bool)

  data = dataframe.values[:, 1:].astype(np.float32)

  test_data = data[int(0.8*SAMPLES_SIZE):,:]
  test_labels = labels[int(0.8*SAMPLES_SIZE):]
  train_data = data[:int(0.8*SAMPLES_SIZE),:]
  train_labels = labels[:int(0.8*SAMPLES_SIZE)]


  # Plot a normal ECG.
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
            epochs=1000, 
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

  # test loss on anomalous data
  anomalus_loss = autoencoder.evaluate(anomalus_data, anomalus_data)
  print("Anomalus loss: ", anomalus_loss)


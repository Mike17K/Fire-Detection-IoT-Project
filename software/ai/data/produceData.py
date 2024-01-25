from matplotlib import pyplot as plt
import numpy as np

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
temperatures_normal = 20+5*smooth_random_changes_2d((SAMPLES_SIZE, NUMBER_OF_SENSORS), 0.1) + 2*np.random.rand(SAMPLES_SIZE, NUMBER_OF_SENSORS)
humidity_normal = 100+50*smooth_random_changes_2d((SAMPLES_SIZE, NUMBER_OF_SENSORS), 0.1) + 2*np.random.rand(SAMPLES_SIZE, NUMBER_OF_SENSORS)
co2_normal = 250+20*smooth_random_changes_2d((SAMPLES_SIZE, NUMBER_OF_SENSORS), 0.1 ) + 2*np.random.rand(SAMPLES_SIZE, NUMBER_OF_SENSORS)

data_normal = np.concatenate((temperatures_normal, humidity_normal, co2_normal), axis=1)

labels_normal = np.zeros((SAMPLES_SIZE, 1))

# Create Anomalous Dataset Dummy
temperatures_anomalous = 40+23*smooth_random_changes_2d((SAMPLES_SIZE, NUMBER_OF_SENSORS), 0.1)+ 2*np.random.rand(SAMPLES_SIZE, NUMBER_OF_SENSORS)
humidity_anomalous = 20+10*smooth_random_changes_2d((SAMPLES_SIZE, NUMBER_OF_SENSORS), 0.1)+ 2*np.random.rand(SAMPLES_SIZE, NUMBER_OF_SENSORS)
co2_anomalous = 400+100*smooth_random_changes_2d((SAMPLES_SIZE, NUMBER_OF_SENSORS), 0.1)+ 2*np.random.rand(SAMPLES_SIZE, NUMBER_OF_SENSORS)

data_anomalous = np.concatenate((temperatures_anomalous, humidity_anomalous, co2_anomalous), axis=1)

labels_anomalous = np.ones((SAMPLES_SIZE, 1))

# Concatenate the normal and anomalous observations
data = np.concatenate((data_normal, data_anomalous), axis=0)
labels = np.concatenate((labels_normal, labels_anomalous), axis=0)

# suffle data
p = np.random.permutation(len(data))
data = data[p]
labels = labels[p]

combined_data = np.concatenate((labels, data), axis=1)

# for each column, find the min and max value and normalize the data of the column
for i in range(1, combined_data.shape[1]):
    min_val = np.min(combined_data[:,i])
    max_val = np.max(combined_data[:,i])
    combined_data[:,i] = (combined_data[:,i] - min_val) / (max_val - min_val)

# combine data and labels, with labels as first column

filepath = "\\".join(__file__.split("\\")[:-1])+f"\\data.csv"
# write data to file
np.savetxt(filepath, combined_data, delimiter=",")

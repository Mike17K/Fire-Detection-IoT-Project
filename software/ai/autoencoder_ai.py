from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model, load_model
import numpy as np

# Define the architecture of the autoencoder
def build_autoencoder(input_dim, encoding_dim):
    # Encoder
    input_layer = Input(shape=(input_dim,))
    encoded = Dense(encoding_dim, activation='relu')(input_layer)

    # Decoder
    decoded = Dense(input_dim, activation='sigmoid')(encoded)

    # Create autoencoder model
    autoencoder = Model(inputs=input_layer, outputs=decoded)

    # Compile the model
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

    return autoencoder

# Set the input dimension and encoding dimension
# Each sensor gives 3 values ( temperature, humidity, co2 ) we will take the closest 10 sensors to analyze # TODO add position
input_dim = 10 * 3 # Adjust this based on your input data dimensionality
encoding_dim = 32  # Choose the size of the encoding layer

# Build the autoencoder model
# Load the model

try:
    autoencoder = load_model('software/ai/autoencoder.h5')
    print("Model found, loading it")
except:
    autoencoder = build_autoencoder(input_dim, encoding_dim)
    print("No model found, creating a new one")



# Display the summary of the model architecture
autoencoder.summary()


def train_autoencoder(autoencoder, X_train, X_test, batch_size, epochs):
    # Train the autoencoder
    autoencoder.fit(X_train, X_train,
                    epochs=epochs,
                    batch_size=batch_size,
                    shuffle=True,
                    validation_data=(X_test, X_test))

    return autoencoder

# Set the batch size and number of epochs
batch_size = 128
epochs = 10

# Create Dataset Dummy
train_tem = 20+5*np.random.rand(1000, 10)
train_tem/=100.0

train_hum = 100+np.random.rand(1000, 10)
train_hum/=200.0

train_co2 = 250+20*np.random.rand(1000, 10)
train_co2/=500.0

X_train = np.concatenate((train_tem, train_hum, train_co2), axis=1)

train_tem = np.array([[20,21,22,20,18,22,21,22,23,22],[20,21,56,58,24,60,70,15,23,22]],dtype=float)
train_tem /= 100.0

train_hum = np.array([[100,101,102,100,98,102,101,102,103,102],[100,101,156,158,124,160,170,115,123,122]],dtype=float)
train_hum /= 200.0

train_co2 = np.array([[250,251,252,250,248,252,251,252,253,252],[250,251,256,258,224,260,270,215,223,222]],dtype=float)
train_co2 /= 500.0

X_test = np.concatenate((train_tem, train_hum, train_co2), axis=1)

# Train the autoencoder model
autoencoder = train_autoencoder(autoencoder, X_train, X_test, batch_size, epochs)

# Save the model
autoencoder.save('software/ai/autoencoder.h5')

# Predict the autoencoder output from test data
predictions = autoencoder.predict(X_test)

# Display the predictions
print(predictions)


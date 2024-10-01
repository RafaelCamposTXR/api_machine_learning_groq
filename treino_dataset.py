import tensorflow as tf
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense

# Load and preprocess your dataset
train_data, val_data = ...  # load and preprocess your dataset

# Create a TensorFlow dataset
train_dataset = tf.data.Dataset.from_tensor_slices((train_data['input_ids'], train_data['labels']))
val_dataset = tf.data.Dataset.from_tensor_slices((val_data['input_ids'], val_data['labels']))

# Define the model architecture
model = Sequential([
    Embedding(input_dim=10000, output_dim=128, input_length=max_length),
    LSTM(64),
    Dense(64, activation='relu'),
    Dense(1)
])

# Compile the model
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

# Train the model
history = model.fit(train_dataset, epochs=10, validation_data=val_dataset)

# Evaluate the model
loss, accuracy = model.evaluate(val_dataset)
print(f'Validation loss: {loss:.3f}, Validation accuracy: {accuracy:.3f}')
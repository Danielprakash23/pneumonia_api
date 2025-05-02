import medmnist
from medmnist import ChestMNIST
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Load ChestMNIST dataset
data_flag = 'chestmnist'
download = True  # Set to False if already downloaded
dataset = ChestMNIST(split='train', download=download)
test_dataset = ChestMNIST(split='test', download=download)

# Extract images and labels
X_train, y_train = dataset.imgs, dataset.labels
X_test, y_test = test_dataset.imgs, test_dataset.labels

# Convert images from uint8 to float32 and normalize (0-1)
X_train = X_train.astype("float32") / 255.0
X_test = X_test.astype("float32") / 255.0

# Expand dimensions to fit CNN input shape (num_samples, 28, 28, 1)
X_train = np.expand_dims(X_train, axis=-1)
X_test = np.expand_dims(X_test, axis=-1)

# Convert 14-class labels to a binary classification (presence of any abnormality)
y_train = (np.sum(y_train, axis=1) > 0).astype("float32")  # Convert multi-label to binary
y_test = (np.sum(y_test, axis=1) > 0).astype("float32")

# Split training data into train & validation sets (80% train, 20% validation)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Define CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')  # Binary classification (Pneumonia vs. Normal)
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=5, validation_data=(X_val, y_val), batch_size=32)

# Evaluate the model on test data
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"\nTest Accuracy: {test_acc:.4f}")

# Save the trained model
model.save("app/model.h5")
print("Model saved as app/model.h5")
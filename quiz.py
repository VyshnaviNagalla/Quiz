# -*- coding: utf-8 -*-
"""Quiz.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rtxFNTLW3LsrXjv6hz1AyDohzwBLXOOi
"""

!pip list | grep tensorflow
!pip list | grep keras
!pip install scikeras

import tensorflow as tf

# Load the MNIST dataset
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=5, validation_data=(test_images, test_labels))

test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f"Test accuracy: {test_acc:.4f}")

!pip install scikeras
!pip install scikit-learn

import pandas as pd
import numpy as np
import tensorflow as tf
from keras.datasets import mnist
from keras.utils import to_categorical

# Load the dataset
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Normalizing the images
X_train = X_train.astype('float32') / 255.0
X_test = X_test.astype('float32') / 255.0

# Reshape data to fit the model input
X_train = np.expand_dims(X_train, -1)
X_test = np.expand_dims(X_test, -1)

# one-hot encoding
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# 2) Building CNN using Keras Sequential model
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.optimizers import Adam, SGD

def build_model(learning_rate=0.001, optimizer='adam'):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation='softmax'))

    if optimizer == 'adam':
        opt = Adam(learning_rate=learning_rate)
    elif optimizer == 'sgd':
        opt = SGD(learning_rate=learning_rate)

    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# 3) Training CNN  on the MNIST dataset
model = build_model()
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Using callbacks
from keras.callbacks import ReduceLROnPlateau, EarlyStopping

reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.001)
early_stopping = EarlyStopping(monitor='val_loss', patience=5)

history = model.fit(X_train, y_train, validation_split=0.2, epochs=10, batch_size=32, callbacks=[reduce_lr, early_stopping])

# 4) Evaluating the model's performance on the test set and report accuracy
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f'Test accuracy: {test_acc:.4f}')

# 5) Using grid search to optimize hyperparameters
learning_rates = [0.001]
batch_sizes = [32, 64]
optimizers = ['adam', 'sgd']

best_accuracy = 0
best_lr = 0
best_batch = 0
best_optimizer = ''

for lr in learning_rates:
    for batch_size in batch_sizes:
        for optimizer in optimizers:
            model = build_model(learning_rate=lr, optimizer=optimizer)
            history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=5, batch_size=batch_size, verbose=0)
            accuracy = np.max(history.history['val_accuracy'])
            print(f"LR={lr}, Batch={batch_size}, Optimizer={optimizer}, Val Accuracy={accuracy:.4f}")

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_lr = lr
                best_batch = batch_size
                best_optimizer = optimizer

print(f"Best parameters: LR={best_lr}, Batch={best_batch}, Optimizer={best_optimizer}, with accuracy={best_accuracy:.4f}")

# 6) Training the best model
best_model = build_model(learning_rate=best_lr, optimizer=best_optimizer)
best_model.compile(optimizer=best_optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Training the model with the best parameters
history = best_model.fit(X_train, y_train, validation_split=0.2, epochs=50, batch_size=best_batch, callbacks=[reduce_lr, early_stopping])

# Evaluate the best model
test_loss, test_acc = best_model.evaluate(X_test, y_test)
print(f'Test accuracy of best model: {test_acc:.4f}')

# 7)history object for result visualization
import matplotlib.pyplot as plt

# Plotting training & validation accuracy values
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Validation'], loc='upper left')

# Plotting training & validation loss values
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Train', 'Validation'], loc='upper left')

plt.show()
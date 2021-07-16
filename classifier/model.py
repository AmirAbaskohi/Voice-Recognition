import json
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras import optimizers
from tensorflow.python.platform.tf_logging import error


DATA_PATH = "data.json"
MODEL_PATH = "model.h5"
LEARNING_RATE = 0.0001
BATCH_SIZE = 32
EPOCHS = 40

def load_data(data_path):
    
    with open(data_path, "r") as data_file:
        data = json.load(data_file)

    X = np.array(data["MFCCs"])
    y = np.array(data["labels"])

    return X, y

def get_number_mappings(data_path):

    with open(data_path, "r") as data_file:
        data = json.load(data_file)

    return len(data["mappings"])
    

def split_data(data_path, test_size=0.1, valid_size=0.1):
    
    X, y = load_data(data_path) 

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=valid_size)

    X_train = X_train[..., np.newaxis]
    X_valid = X_valid[..., np.newaxis]
    X_test = X_test[..., np.newaxis]

    return X_train, X_valid, X_test, y_train, y_valid, y_test

def build_model(input_shape, number_of_mappings, lr, loss="sparse_categorical_crossentropy"):

    model = tf.keras.Sequential()

    model.add(tf.keras.layers.Conv2D(64, (3, 3), activation="relu",
                                 input_shape=input_shape,
                                 kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding="same"))

    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation="relu",
                                 input_shape=input_shape,
                                 kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding="same"))

    model.add(tf.keras.layers.Conv2D(32, (2, 2), activation="relu",
                                 input_shape=input_shape,
                                 kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPool2D((2, 2), strides=(2, 2), padding="same"))

    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(64, activation="relu"))
    model.add(tf.keras.layers.Dropout(0.3))

    model.add(tf.keras.layers.Dense(number_of_mappings, activation="softmax"))

    optimiser = tf.optimizers.Adam(learning_rate=lr)
    model.compile(optimizer=optimiser,
                  loss=loss,
                  metrics=["accuracy"])

    model.summary()
    return model



def train_model():
    
    X_train, X_valid, X_test, y_train, y_valid, y_test = split_data(DATA_PATH)

    # We have three dimensions for our CNN
    # First one is segments
    # Second one is cofficents
    # The last one is 
    input_shape = (X_train.shape[1], X_train.shape[2], X_train.shape[3])
    number_of_mappings = get_number_mappings(DATA_PATH)
    print(input_shape)
    model = build_model(input_shape, number_of_mappings, LEARNING_RATE)

    model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_data=(X_valid, y_valid))

    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"loss: {loss}, accuracy:{accuracy}")

    model.save(MODEL_PATH)

if __name__ == "__main__":
    train_model()
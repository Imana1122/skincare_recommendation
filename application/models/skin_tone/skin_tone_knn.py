"""
To classify the input skin into one of the 6 skin tones
"""
import pandas as pd
import os
from sklearn.neighbors import KNeighborsClassifier
from models.skin_tone.skin_detection import skin_detection

def identify_skin_tone(image_path, dataset):
    # Get the mean color values of the skin from the image using skin_detection function
    mean_color_values = skin_detection(image_path)

    # Read the skin tone dataset into a DataFrame
    df = pd.read_csv(dataset)

    # Extract features (RGB values) and labels from the dataset
    X = df.iloc[:, [1, 2, 3]].values
    y = df.iloc[:, 0].values

    # Create a KNeighborsClassifier with 6 neighbors and Euclidean distance metric
    classifier = KNeighborsClassifier(n_neighbors=6, metric='minkowski', p=2)

    # Train the classifier on the dataset
    classifier.fit(X, y)

    # Prepare the test data (mean color values of the input skin)
    X_test = [mean_color_values]

    # Predict the skin tone using the trained classifier
    y_pred = classifier.predict(X_test)
    return y_pred[0]

"""
To classify the input skin into one of the 6 skin tones
"""
import pandas as pd
import os
import cv2
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
from models.skin_tone.skin_detection import skin_detection

def identify_skin_tone(image_path, dataset):
    # Load the dataset into a DataFrame
    dataset = pd.read_csv(r'C:\Users\imana\CW AI\Skyn\application\models\skin_tone\skin_tone_dataset.csv')
    y = skin_detection(image_path)
    # Extract RGB values from the dataset
    values_vector = dataset.iloc[:, [1, 2, 3]].values
    # Repeat the input skin tone vector to create a matrix
    input_mat = np.repeat(y[np.newaxis, :], len(dataset.index), axis=0)

    # Calculate Euclidean distances between input and dataset
    distances = euclidean_distances(values_vector, input_mat)

    # Calculate similarity scores by taking the inverse of distances
    similarities = 1 / (1 + distances)

    # Create a new column 'ds' in the dataframe dataset and assign the first column of the similarities matrix
    dataset['ds'] = similarities[:, 0]
    dataset.sort_values(by=['ds'], ascending=False, inplace=True)

    # Sort the dataframe dataset based on the 'ds' column in descending order
    dataset = dataset.sort_values(by=['ds'], ascending=False)

    # Return the 'Type' value of the first row in the sorted dataframe dataset
    return dataset.sort_values(by=['ds'], ascending=False).iloc[0]['Type']

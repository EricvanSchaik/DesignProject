import csv
from datetime import datetime

import numpy as np
import pandas as pd

from data_import.import_data import parse_csv, parse_header


label_dict = {
    "lying": 1,
    "standing": 2,
    "walking-rider": 3,
    "walking-natural": 4,
    "trotting-rider": 5,
    "trotting-natural": 6,
    "running-rider": 7,
    "running-natural": 8,
    "grazing": 9,
    "eating": 10,
    "fighting": 11,
    "shaking": 12,
    "scratch-biting": 13,
    "breast-feeding": 14,
    "rubbing": 15,
    "unknown": 16,
    "food-fight": 17,
    "head-shake": 18,
    "rolling": 19,
    "scared": 20,
    "jumping": 21
}


def add_labels_to_data(sensor_data: pd.DataFrame, label_data: [], label_col: str, timestamp_col: str, label_dict: {}):
    """
    Add a label column to a DataFrame and fill it with provided labels.
    
    :param sensor_data: The sensor data.
    :param label_data: A list consisting of labels and timestamps, with the label at index <i>0</i> and the timestamp
        at index <i>1</i>. The list should be sorted by timestamp.
    :param label_col: The name of the label column.
    :param timestamp_col: The name of the timestamp column.
    :param label_dict: A dictionary mapping label strings to their corresponding integer values.
    :return: Sensor data DataFrame where a label column has been added.
    """
    TIME_INDEX = 0
    LABEL_INDEX = 1

    df = sensor_data.copy()

    # Add Label column to the DataFrame and initialize it to NaN
    df[label_col] = np.nan

    prev_timestamp = label_data[0][TIME_INDEX]
    prev_label = None

    for label_entry in label_data:
        timestamp = label_entry[TIME_INDEX]
        label_str = label_entry[LABEL_INDEX]

        # Convert label string to corresponding integer
        label = label_dict[label_str]

        if prev_label:
            # Add label to the corresponding rows in the sensor data
            df.loc[
                (df[timestamp_col] >= prev_timestamp) & (sensor_data[timestamp_col] < timestamp),
                label_col
            ] = prev_label

        prev_timestamp = timestamp
        prev_label = label

    # Drop rows where the label is NaN (no label data available)
    res = df.dropna(subset=[label_col])

    return res

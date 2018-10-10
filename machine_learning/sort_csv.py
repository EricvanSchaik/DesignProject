import csv
from datetime import datetime
from enum import Enum

import numpy as np
import pandas as pd

from data_import.import_data import parse_csv, parse_header


class Label(Enum):
    lying: 1
    standing: 2
    walking_rider: 3
    walking_natural: 4
    trotting_rider: 5
    trotting_natural: 6
    running_rider: 7
    running_natural: 8
    grazing: 9
    eating: 10
    fighting: 11
    shaking: 12
    scratch_biting: 13
    breast_feeding: 14
    rubbing: 15
    unknown: 16
    food_fight: 17
    head_shake: 18
    rolling: 19
    scared: 20
    jumping: 21


def get_data():
    labels = csv.reader(open('../data/20180515_09-58_CCDC301661B33D7_labels.csv'), delimiter=',')
    next(labels)  # Skip header
    sorted_labels = sorted(labels, key=lambda row: row[0])

    sensor_data = parse_csv('../data/20180515_09-58_CCDC301661B33D7_sensor.csv')
    headers = parse_header('../data/20180515_09-58_CCDC301661B33D7_sensor.csv')
    sensor_data['Label'] = np.nan
    sensor_start_time = datetime.strptime(headers[2][1] + headers[2][2], '%Y-%m-%d%H:%M:%S.%f')

    # Add timestamp column to sensor data
    sensor_data['Time'] = pd.to_timedelta(sensor_data['Time'], unit='s')
    sensor_data['Timestamp'] = sensor_data['Time'] + sensor_start_time
    sensor_data = sensor_data.set_index('Time')

    # Add ground truth labels to the sensor data
    prev_time = datetime.strptime(sorted_labels[0][0], '%Y%m%d %H:%M:%S.%f')
    prev_label = None

    for label_point in sorted_labels:
        timestamp = datetime.strptime(label_point[0], '%Y%m%d %H:%M:%S.%f')
        label = label_point[1]

        if prev_label:
            sensor_data.loc[
                (sensor_data['Timestamp'] >= prev_time) & (sensor_data['Timestamp'] < timestamp),
                'Label'
            ] = prev_label

        prev_time = timestamp
        prev_label = label

    # Drop rows where the label is NaN
    res = sensor_data.dropna(subset=['Label'])

    # Drop rows where the label is 'unknown'
    res = res[res.Label != 'unknown']

    return res


def sliding_window(sensor_data: pd.DataFrame):
    sensor_data = sensor_data.drop(['Mx', 'My', 'Mz', 'T', 'Label', 'Timestamp'], axis=1)
    return sensor_data.rolling(100).mean()


print(sliding_window(get_data()))

import csv
from datetime import datetime

import numpy as np
import pandas as pd

from data_import.import_data import parse_csv, parse_header

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

prev_time = datetime.strptime(sorted_labels[0][0], '%Y%m%d %H:%M:%S.%f')

for label_point in sorted_labels:
    timestamp = datetime.strptime(label_point[0], '%Y%m%d %H:%M:%S.%f')
    label = label_point[1]

    old = prev_time
    new = timestamp

    sensor_data.loc[(sensor_data['Timestamp'] >= prev_time) & (sensor_data['Timestamp'] < timestamp), 'Label'] = label
    
    # test = (sensor_data['Timestamp'] >= prev_time) & (sensor_data['Timestamp'] < timestamp)
    # print(test[test == True])

    prev_time = timestamp
    break

print(sensor_data['Label'])

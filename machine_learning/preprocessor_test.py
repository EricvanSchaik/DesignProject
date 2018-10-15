from machine_learning import preprocessor as pp
from data_import import label_data as ld
from data_import import sensor_data as sd
from data_import import sensor_data_test as sdt
from datastorage import labelstorage as ls

import csv
import pandas as pd
import datetime as dt


SENSOR_FILE = 'data/20180515_09-58_CCDC301661B33D7_sensor.csv'
PROJECT_DIR = 'test_project'
SENSOR_ID = 'CCDC301661B33D7'

sensor_data = sd.SensorData(SENSOR_FILE, sdt.test_settings())
label_manager = ls.LabelManager(PROJECT_DIR)
label_data = ld.LabelData(SENSOR_ID, label_manager)

labels = label_data.get_labels()

res = []

for i in range(len(labels) - 1):
    res.append([labels[i][0], labels[i + 1][0], labels[i][1]])


def add_timestamp_column(sensor_data: pd.DataFrame, base_datetime: dt.datetime, time_col: str, timestamp_col,
                         time_unit='s'):
    res = sensor_data.copy()
    res[timestamp_col] = pd.to_timedelta(res[time_col], unit=time_unit) + base_datetime

    return res


base_datetime = sensor_data.metadata['datetime']

sensor_data = add_timestamp_column(sensor_data.data, base_datetime, 'Time', 'Timestamp')
preprocessed = pp.add_labels_to_data(sensor_data, res, 'Label', 'Timestamp')

print(preprocessed['Timestamp'])

# print(label_manager.get_all_labels('SN:CCDC3016AE9D6B4'))

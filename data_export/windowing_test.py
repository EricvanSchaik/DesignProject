import csv
from data_import import sensor_data as sd
from data_import.sensor_data_test import test_settings as settings
from machine_learning import preprocessor as pp
import pandas as pd
from data_export import windowing as w
from datetime import timedelta


def test_sensor_data():
    sensor_data = sd.SensorData("../data/20180515_09-58_CCDC301661B33D7_sensor.csv", settings())
    file = open('../data/20180515_09-58_CCDC301661B33D7_labels.csv')
    labels = csv.reader(file)
    next(labels)
    labels = sorted(labels, key=lambda row: row[0])

    res = []
    for i in range(len(labels) - 1):
        res.append([labels[i][0], labels[i + 1][0], labels[i][1]])

    sensor_data.data['Timestamp'] = pd.to_timedelta(
        sensor_data.data['Time'], unit='s') + sensor_data.metadata['datetime']
    return pp.add_labels_to_data(sensor_data.data, res, 'Label', 'Timestamp')


def windowing_test():
    df = test_sensor_data()
    print("data frame constructed")

    dfs = w.split_df(df, 'Label')

    print("data frame split, length:", len(dfs))

    for df in dfs:
        if len(df) < 1000:
            continue
        rolled = df.resample('2s', on='Timestamp').mean()
        print("Label:", df['Label'].iloc[0])
        print(rolled)


def windowing_2_test():
    df = test_sensor_data()
    print("DataFrame constructed")

    res = w.windowing_2(df, 'Label', 'Timestamp')
    print(res)


def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))


windowing_2_test()

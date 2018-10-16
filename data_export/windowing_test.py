import csv
from data_import import sensor_data as sd
from data_import.sensor_data_test import test_settings as settings
from machine_learning import preprocessor as pp
import pandas as pd
from data_export import windowing as w
from datetime import timedelta, datetime


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


def resample_test():
    timestamps = []
    for i in range(20):
        timestamps.append(datetime(2000, 1, 1, 0, 0, 0) + timedelta(milliseconds=i*500))
    df = pd.DataFrame({'Timestamp': timestamps,
                       'Data': list(range(20))})

    df1 = df.rolling(window='2s', on='Timestamp').mean()
    print(df)
    print(df1)

    start = df['Timestamp'].iloc[0]
    pivot = start + timedelta(seconds=1)
    cutoff = df.loc[df['Timestamp'] == nearest(df['Timestamp'].tolist(), pivot)]
    rps = cutoff.index[0] - df.index[0]
    print('rows per second:', rps)

    df2 = df1[rps*2 - 1::rps*2]
    df3 = df1[rps*3 - 1::rps*2]

    print(df2)
    print(df3)
    print(w.zip_df(df2, df3))


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

    res = w.windowing_2(df.head(2010), 'Label', 'Timestamp')
    return res


def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))


print(windowing_2_test())
# resample_test()

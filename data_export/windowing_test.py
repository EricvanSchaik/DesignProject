import csv
import numpy as np
from timeit import timeit

from data_import import sensor_data as sd
from data_import.sensor_data_test import test_settings as settings
import pandas as pd
from data_export import windowing as w
from datetime import timedelta, datetime
from data_export import export_data as ed


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped


def test_sensor_data():
    sensor_data = sd.SensorData("../data/20180515_09-58_CCDC301661B33D7_sensor.csv", settings())
    file = open('../data/20180515_09-58_CCDC301661B33D7_labels.csv')
    labels = csv.reader(file)
    next(labels)
    labels = sorted(labels, key=lambda row: row[0])

    res = []
    for i in range(len(labels) - 1):
        res.append([labels[i][0], labels[i + 1][0], labels[i][1]])

    sensor_data.add_timestamp_column('Time', 'Timestamp')
    sensor_data.add_labels(res, 'Label', 'Timestamp')

    return sensor_data.get_data()


def small_data_test():
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

    df2 = df1[rps*2 - 1::rps]
    print(df2)


def windowing_test():
    df = test_sensor_data()
    print("DataFrame constructed")

    # wrapped = wrapper(w.windowing, df, 'Label', 'Timestamp')
    # print('.mean():', timeit(wrapped, number=1))
    # wrapped = wrapper(w.windowing, df, 'Label', 'Timestamp', w.mean)
    # print('Apply:', timeit(wrapped, number=1))

    res = w.windowing(df, 'Label', 'Timestamp')
    return res


def windowing2_test():
    df = test_sensor_data()
    print("DataFrame constructed")

    # wrapped = wrapper(w.windowing2, df, ['Ax', 'Ay', 'Az'], 'Label', 'Timestamp', mean=np.mean, std=np.std)
    # print('mean: ', timeit(wrapped, number=1))
    return w.windowing2(df, ['Ax', 'Ay', 'Az'], 'Label', 'Timestamp', mean=np.mean, std=np.std)


def windowing3_test():
    df = test_sensor_data()
    print("DataFrame constructed")

    funcs = {
        'mean': {
            w.STR_FUNC: np.mean,
            w.STR_COLS: ['Ax', 'Ay', 'Az']
        },
        'std': {
            w.STR_FUNC: np.std,
            w.STR_COLS: ['Ax', 'Ay', 'Az']
        }
    }
    wrapped = wrapper(w.windowing3, df, funcs, 'Label', 'Timestamp', True)
    print('mean: ', timeit(wrapped, number=1))
    return w.windowing3(df, funcs, 'Label', 'Timestamp')


def windowing2vs4():
    df = test_sensor_data()
    print('DataFrame constructed')

    wrapped2 = wrapper(w.windowing2, df, ['Ax', 'Ay', 'Az'], 'Label', 'Timestamp', mean=np.mean, std=np.std)
    wrapped4 = wrapper(w.windowing4, df, ['Ax', 'Ay', 'Az'], 'Label', 'Timestamp', mean=np.mean, std=np.std)

    time2 = timeit(wrapped2, number=1)
    time4 = timeit(wrapped4, number=1)

    print('windowing2:', time2)
    print('windowing4:', time4)


def windowing5_test():
    df = test_sensor_data()
    print("DataFrame constructed")

    # Time test
    wrapped = wrapper(w.windowing5, df, ['Ax', 'Ay', 'Az'])
    print('windowing5:', timeit(wrapped, number=1))

    # return w.windowing5(df, ['Ax', 'Ay', 'Az'])


def export_test():
    df = test_sensor_data()
    print("DataFrame constructed")

    ed.export([df], 'Label', 'Timestamp', '../data/test_export.csv', [])


def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))


if __name__ == '__main__':
    # df1 = windowing2_test()
    # df2 = windowing3_test()
    export_test()
    # windowing2vs4()
    # print(windowing5_test())

    # ed.export([df.drop(columns='Time')], '../data/export_test.csv')

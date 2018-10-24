import random
from timeit import timeit
from datetime import timedelta, datetime

import pandas as pd
from data_import import sensor_data as sd
from data_import.sensor_data_test import test_settings as settings
from data_export import windowing as w


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def test_df():
    sensor_data = sd.SensorData("../data/DATA-001.CSV", settings())
    data = sensor_data.get_data()
    size = len(data)
    labels = ['A', 'B']
    data['Label'] = pd.Series(random.choice(labels) for _ in range(size))
    return data


def time_df():
    t = [0.006042, 0.006378, 0.015350, 0.015717, 0.016052,
         0.025360, 0.035370, 0.045441, 0.055389, 0.065399]
    df = pd.DataFrame({'Time': t,
                       'Data': list(range(0, 10)),
                       'Label': ['A', 'A', 'B', 'B', 'B', 'C', 'A', 'A', 'A', 'A']})
    date = '2018-05-15'
    time = '08:54:32.261'
    dt = datetime.strptime(date + time, '%Y-%m-%d%H:%M:%S.%f')
    df['Time'] = df['Time'].map(lambda x: dt + timedelta(seconds=x))
    return df


def drop_column(df, col):
    return df.drop(col, axis=1)


def new_df_without_column(df):
    collist = df.columns.tolist()
    return df[collist[:-1]]


df = test_df()
print('DataFrame constructed')

wrapped1 = wrapper(drop_column, df, 'Label')
wrapped2 = wrapper(new_df_without_column, df)
t1 = timeit(wrapped1, number=1000)
# t2 = timeit(wrapped2, number=1000)
print("drop:", t1)
# print("new df:", t2)


# wrapped = wrapper(w.split_df, df, 'Label')
# t = timeit(wrapped, number=1)
# print('split_df():', t)

# result = w.split_df(df, 'Label')

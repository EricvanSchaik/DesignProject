from timeit import timeit

import pandas as pd
from data_export import windowing as ed
from datetime import datetime, timedelta
from data_import import sensor_data as sd
from data_import.sensor_data_test import test_settings as settings
import random


def time():
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


def test_df():
    sensor_data = sd.SensorData("../data/DATA-001.CSV", settings())
    size = len(sensor_data.data)
    labels = ['A', 'A', 'B']
    sensor_data.data['Label'] = pd.Series(random.choice(labels) for _ in range(size))
    return sensor_data.data


def test():
    df = test_df()
    print('DataFrame constructed')

    result = ed.split_df(df, 'Label')
    print('DataFrame split:', len(result))

    def loop():
        for r in result:
            # print('Label:', r['Label'].tolist()[0], 'with length:', len(r))
            # print(r)
            collist = r.columns.tolist()
            r = r[collist[:-1]]
            ed.windowing(r, 'Time', 4, 2)
    print(timeit(loop, number=1))


test()

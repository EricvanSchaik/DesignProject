from timeit import timeit
import pandas as pd
from data_import import sensor_data as sd
import math


def column_operation(df, col, func, *args):
    # Applies a function with arguments to a column of the data frame
    df[col] = df[col].apply(lambda x: func(x, args))


def test_data():
    return pd.DataFrame({'a': pd.Series([1, 2, 3], index=['a', 'b', 'c']),
                         'b': pd.Series([4, 5, 6], index=['a', 'b', 'c']),
                         'c': pd.Series([7, 8, 9], index=['a', 'b', 'c'])})


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def time_test():
    # about 2.86 seconds
    wrapped = wrapper(sd.SensorData, "../data/DATA-001.CSV")
    print(timeit(wrapped, number=5)/5)


def test_settings():
    settings = dict()
    settings['time_row'], settings['time_col'] = 3, 3
    settings['date_row'], settings['date_col'] = 3, 2
    settings['sr_row'], settings['sr_col'] = 5, 2
    settings['sn_row'], settings['sn_col'] = 2, 5
    settings['names_row'] = 8
    settings['comment'] = ';'

    names = ["Time", "Ax", "Ay", "Az", "Gx", "Gy", "Gz", "Mx", "My", "Mz", "T"]
    for name in names:
        settings[name + "_data_type"] = "-"
        settings[name + "_sensor_name"] = "-"
        settings[name + "_sampling_rate"] = "-"
        settings[name + "_unit"] = "-"

    return settings


def vector(row):
    return math.sqrt(row['Ax']**2 + row['Ay']**2 + row['Az']**2)


sett = test_settings()
sensor_data = sd.SensorData("../data/DATA-001.CSV", sett)
print(sensor_data.metadata)
print(sensor_data.data)

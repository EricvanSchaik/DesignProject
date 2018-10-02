from timeit import timeit
import pandas as pd
from data_import import sensor_data as sd


def test_data():
    return pd.DataFrame({'a': pd.Series([1, 2, 3], index=['a', 'b', 'c']),
                         'b': pd.Series([4, 5, 6], index=['a', 'b', 'c']),
                         'c': pd.Series([7, 8, 9], index=['a', 'b', 'c'])})


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def parse_time_test():
    # Time test for creating a SensorData object and parsing a file
    # about 2.86 seconds
    wrapped = wrapper(sd.SensorData, "../data/DATA-001.CSV", test_settings())
    print("parse_time_test():", timeit(wrapped, number=1))


def add_column_time_test():
    # Time test for adding a vector column to the data
    # about 9.26 seconds
    sensor_data = sd.SensorData("../data/DATA-001.CSV", test_settings())
    wrapped = wrapper(sensor_data.add_column, "Vector", "sqrt(Ax^2 + Ay^2 + Az^2)")
    print("add_column_time_test():", timeit(wrapped, number=1))


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

    settings["Ax_conversion"] = "Ax * 9.807 / 4096"
    settings["Ay_conversion"] = "Ay * 9.807 / 4096"
    settings["Az_conversion"] = "Az * 9.807 / 4096"

    settings["Gx_conversion"] = "Gx / 16.384"
    settings["Gy_conversion"] = "Gy / 16.384"
    settings["Gz_conversion"] = "Gz / 16.384"

    settings["Mx_conversion"] = "Mx / 3.413"
    settings["My_conversion"] = "My / 3.413"
    settings["Mz_conversion"] = "Mz / 3.413"

    settings["T_conversion"] = "T / 1000"

    return settings


def add_column_test():
    sens_data = sd.SensorData("../data/DATA-001.CSV", test_settings())
    sens_data.add_column("Vector", "sqrt(Ax^2 + Ay^2 + Az^2)")
    print(sens_data.data[['Ax', 'Ay', 'Az', 'Vector']])


# parse_time_test()
# add_column_time_test()

print("add_column_test():", timeit(add_column_test, number=1))

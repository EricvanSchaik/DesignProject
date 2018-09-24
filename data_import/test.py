from timeit import timeit
import pandas as pd
from data_import import sensor_data as sd


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


random = dict()
random['bier'] = 'bier'
print(random['bier'])
if 'geenbier' not in random:
    random['geenbier'] = None
print(random['geenbier'])

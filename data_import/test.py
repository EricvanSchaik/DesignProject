import pandas as pd
from data_import import function as f


def column_operation(df, col, func, *args):
    # Applies a function with arguments to a column of the data frame
    df[col] = df[col].apply(lambda x: func(x, args))


def test_data():
    return pd.DataFrame({'a': pd.Series([1, 2, 3], index=['a', 'b', 'c']),
                         'b': pd.Series([4, 5, 6], index=['a', 'b', 'c']),
                         'c': pd.Series([7, 8, 9], index=['a', 'b', 'c'])})


def test1():
    df = test_data()
    print(df)
    column_operation(df, 'a', f.add, 2)
    print(df)
    pass


test1()

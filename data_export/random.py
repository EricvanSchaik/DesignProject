import random
from data_export import windowing as w
import pandas as pd


def test_df():
    size = 50
    df = pd.DataFrame(index=range(size), columns=['Time', 'Data', 'Label'])

    labels = ['A', 'B']
    for i in range(size):
        df.loc[i] = [i, i * 2, random.choice(labels)]
    return df


df = test_df()
result = w.split_df(df, 'Label', 'temp')

for r in result:
    print('Label:', r['Label'].tolist()[0], 'with length:', len(r))
    print(r)
    r2 = r.drop('Label', axis=1)
    print(w.windowing(r2, 'Time', 2, 1))

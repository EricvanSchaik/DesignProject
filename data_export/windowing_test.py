import pandas as pd
from data_export import windowing as ed
from datetime import datetime, timedelta


def test_df():
    t = [0.006042, 0.006378, 0.015350, 0.015717, 0.016052,
         0.025360, 0.035370, 0.045441, 0.055389, 0.065399]
    df = pd.DataFrame({'Time': t,
                       'Data': list(range(0, 10)),
                       'Label': ['A', 'A', 'B', 'B', 'B', 'C', 'A', 'A', 'A', 'A']})
    date = '2018-05-15'
    time = '08:54:32.261'
    # dt = datetime.strptime(date + time, '%Y-%m-%d%H:%M:%S.%f')
    # df['Time'] = df['Time'].map(lambda x: dt + timedelta(seconds=x))
    return df


df = test_df()
print(df)

result = ed.split_df(df, 'Label', 'temp')
for r in result:
    print('Label:', r['Label'].tolist()[0], 'with length:', len(r))
    print(r)
    r2 = r.drop('Label', axis=1)
    print(ed.windowing(r2, 'Time', 2, 1))

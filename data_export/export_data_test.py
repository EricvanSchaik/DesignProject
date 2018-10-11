import pandas as pd
from data_export import export_data as ed


def test_df():
    t = ['0.006042', '0.006378', '0.015350', '0.015717', '0.016052',
         '0.025360', '0.035370', '0.045441', '0.055389', '0.065399']
    return pd.DataFrame({'Time': t,
                         'Data': list(range(10, 20)),
                         'Label': ['A', 'A', 'B', 'B', 'B', 'C', 'A', 'A', 'A', 'A']})


def time_to_datetime(timestring, datestring, df):
    # timetd = timedelta(hours=int(timestring[0:2]), minutes=int(timestring[3:5]),
    #                    seconds=int(timestring[6:8]), milliseconds=int(timestring[9:12]))
    # datedt = datetime.strptime(datestring, '%Y-%m-%d')
    # combidt = datedt + timetd
    pass


df = test_df()
print(df)

# TODO: 'Time' column as index

result = ed.split_df(df, 'Label', 'temp')
for r in result:
    print('Label:', r['Label'].tolist()[0], 'with length:', len(r))
    print(r)
    r2 = r.drop('Label', axis=1)
    print(ed.windowing(r2, 'Time', 2))

import pandas as pd
from data_export import export_data as ed


def test_df():
    return pd.DataFrame({'Time': list(range(0, 10)),
                         'A': list(range(0, 10)),
                         'B': list(range(0, 10)),
                         'C': ['A', 'A', 'C', 'C', 'B', 'C', 'C', 'A', 'A', 'A']})


df = test_df()
# df = df.drop('C', axis=1)
print(df)
# new_df = ed.windowing(df, 3)
# print(new_df)

result = ed.split_df(df, 'C', 'D')
for r in result:
    print('Label:', r['C'].tolist()[0], 'with length:', len(r))
    print(r)
    r2 = r.drop('C', axis=1)
    print(ed.windowing(r2, 2))

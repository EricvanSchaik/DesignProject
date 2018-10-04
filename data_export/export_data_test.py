import pandas as pd
from data_export import export_data as ed


def test_df():
    return pd.DataFrame({'Time': list(range(0, 10)),
                         'A': list(range(0, 10)),
                         'B': list(range(0, 10)),
                         'C': ['A', 'A', 'C', 'C', 'B', 'C', 'C', 'A', 'A', 'A']})


df = test_df()
result = ed.split_df(df, 'C', 'D')
for r in result:
    print(r)

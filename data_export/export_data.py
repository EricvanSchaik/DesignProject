import pandas as pd

from data_export import windowing as w


def export(data: [], label_col: str, timestamp_col: str, file_path: str, comments: [str], comment=';'):
    # Write comments to a file and use that as start file for 'to_csv'
    f = open(file_path, 'a')
    for c in comments:
        # TODO: determine whether '\n' needs to be added at the end of the line
        f.write(comment + c)

    res = []

    # Get list of columns to be windowed over
    collist = data[0].columns.tolist()
    collist.remove(label_col)
    collist.remove(timestamp_col)

    # Window over data per DataFrame
    for df in data:
        new_df = w.windowing_fast(df, collist, label_col, timestamp_col)
        res.append(new_df)

    # Turn list into one DataFrame
    df = pd.concat(res)

    # Write DataFrame to a csv file
    df.to_csv(file_path)

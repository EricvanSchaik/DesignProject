import pandas as pd
import os

from data_export import windowing as w


def export(data: [], label_col: str, timestamp_col: str, file_path: str, comments: [str], comment=';'):
    # Initialise result list
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

    # Remove file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)

    # Write comments to a file and use that as start file for 'to_csv'
    f = open(file_path, 'a')
    for c in comments:
        f.write(comment + c + '\n')

    # Write DataFrame to the file
    df.to_csv(f)

    # Close the file
    f.close()

from datetime import timedelta

import pandas as pd


def split_df(df, col):
    """
    Splits a data frame into multiple data frames based on the given column; if the column value
    changes, a new data frame is created. Changes are stored in a temporary pandas Series,
    which has a False value for every new value in the given column.

    :param df: The data frame that will be split up
    :param col: The column that determines the split locations
    :return: A list with the split data frames
    """
    # Create boolean column where every False signals a new value
    temp = df[col].eq(df[col].shift())

    # Create a difference data frame with only the rows
    # of the changed values
    df_diff = df[temp == 0]

    # Get the difference data frame index
    idx = df_diff.index.tolist()

    # Determine last index of original data frame
    last = df.index.tolist()[-1]

    result = []
    for i in range(len(idx) - 1):
        # Slice original data frame from changed value until the next
        new_df = df.loc[idx[i]:idx[i + 1] - 1]

        # Add data frame to result list
        result.append(new_df)

    # Slice the last part of the data frame and add it to the result list
    last_df = df.loc[idx[len(idx) - 1]:last]
    result.append(last_df)
    return result


def zip_df(df1, df2):
    """
    --Deprecated--
    Zips two data frames together alternately.

    :param df1: The first data frame. Its first row will be the first row in the resulting data frame.
    :param df2: The second data frame. Its first row will be the second row in the resulting data frame.
    :return: A zipped data frame from df1 and df2
    """
    # Determine length of new data frame
    new_len = len(df1) + len(df2)

    # Create shell of new data frame
    df = pd.DataFrame(index=range(new_len), columns=list(df1))

    # Iterate over both data frames
    pointer1, pointer2 = 0, 0
    for i in range(new_len):
        if i % 2 == 0:
            # Even, so a row from df1 is added
            df.iloc[i] = df1.iloc[pointer1].tolist()
            pointer1 += 1
        else:
            # Odd, so a row from df2 is added
            df.iloc[i] = df2.iloc[pointer2].tolist()
            pointer2 += 1
    return df


def nearest(items, pivot):
    """
    Finds the item in a list of items closest to a pivot.
    :param items: List of items
    :param pivot: Pivot looked for in the list.
    :return: Item in the list closest to the pivot.
    """
    return min(items, key=lambda x: abs(x - pivot))


def windowing(df, label_col, timestamp_col):
    """
    Windows over a DataFrame by splitting it into segments based on the label column and
    windowing over every segment separately.
    :param df: The DataFrame to be windowed over.
    :param label_col: The column containing the labels.
    :param timestamp_col: The column containing the timestamps.
    :return: A windowed DataFrame with the timestamp as index
    """
    # Split DataFrame by label
    dfs = split_df(df, label_col)

    # Initialise list to store results
    res = []

    # Window over every DataFrame in the dfs list
    for df in dfs:
        # Determine label of DataFrame
        label = df[label_col].iloc[0]

        # Remove label column
        df = df[df.columns.tolist()[:-1]]

        # Determine index of timestamp 1 second after starting timestamp
        pivot = df[timestamp_col].iloc[0] + timedelta(seconds=1)
        cutoff = df.loc[df[timestamp_col] == nearest(df[timestamp_col].tolist(), pivot)]

        # Determine rows per second of DataFrame
        rps = cutoff.index[0] - df.index[0]

        # Window over DataFrame
        # TODO: Allow custom function
        new_df = df.rolling(window='2s', on='Timestamp').mean()

        # Slice DataFrame to get correct windows with overlap
        new_df = new_df[rps*2 - 1:: rps]

        # Add label column again
        new_df[label_col] = label

        # Add resulting DataFrame to list
        res.append(new_df)

    # Concatenate DataFrames from list into one single DataFrame and return it
    return pd.concat(res).set_index(timestamp_col)

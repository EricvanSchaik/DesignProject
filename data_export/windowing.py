from datetime import timedelta

import pandas as pd


STR_FUNC = 'function'
STR_FUNCS = 'functions'
STR_COLS = 'columns'


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


def nearest(items, pivot):
    """
    Finds the item in a list of items closest to a pivot.
    :param items: List of items
    :param pivot: Pivot looked for in the list.
    :return: Item in the list closest to the pivot.
    """
    return min(items, key=lambda x: abs(x - pivot))


def windowing(df: pd.DataFrame, cols: [str], label_col: str, timestamp_col: str, **funcs):
    """
    Windows over a DataFrame by splitting it into segments based on the label column and
    windowing over every segment separately.

    :param df: The DataFrame to be windowed over.
    :param cols: The columns that should be used for windowing.
    :param label_col: The column containing the labels.
    :param timestamp_col: The column containing the timestamps.
    :param funcs: A dictionary of function names and functions.
    :return: A windowed DataFrame with the timestamp as index.
    """
    # Split DataFrame by label
    split_dfs = split_df(df, label_col)

    # Initialise list to store results
    res = []

    # Window over every DataFrame in the dfs list
    for df in split_dfs:
        # Determine label of DataFrame
        label = df[label_col].iloc[0]
        df_rolls = []

        # Determine index of timestamp 1 second after starting timestamp
        pivot = df[timestamp_col].iloc[0] + timedelta(seconds=1)
        cutoff = df.loc[df[timestamp_col] == nearest(df[timestamp_col].tolist(), pivot)]

        # Determine rows per second of DataFrame
        rps = cutoff.index[0] - df.index[0]

        for col in cols:
            df_col = df[[col, timestamp_col]]

            if funcs:
                for func_name, func in funcs.items():
                    new_col = '%s_%s' % (col, func_name)

                    df_roll = df_col.rolling(window='2s', on=timestamp_col).apply(func, raw=True)
                    df_roll = df_roll.rename(columns={col: new_col})
                    df_roll = df_roll[rps*2 - 1::rps]

                    df_rolls.append(df_roll)
            else:
                # Use the mean as the standard function
                new_col = '%s_%s' % (col, 'mean')

                df_roll = df_col.rolling(window='2s', on=timestamp_col).mean()
                df_roll = df_roll.rename(columns={col: new_col})
                df_roll = df_roll[rps * 2 - 1::rps]

                df_rolls.append(df_roll)

        timestamps = df_rolls[0][timestamp_col]

        for df_roll in df_rolls:
            df_roll.drop(timestamp_col, axis=1, inplace=True)

        df_rolls = pd.concat(df_rolls, axis=1)
        df_rolls[label_col] = label
        df_rolls[timestamp_col] = timestamps

        res.append(df_rolls)

    # Concatenate DataFrames from list into one single DataFrame and return it
    return pd.concat(res).set_index(timestamp_col).sort_index(axis=1).sort_index(axis=0)


def windowing_fast(df: pd.DataFrame, cols: [str], label_col='Label', timestamp_col='Timestamp'):
    """
    Windows over a DataFrame by splitting it into segments based on the label column and
    windowing over every segment separately.

    :param df: The DataFrame to be windowed over.
    :param cols: The columns that should be used for windowing.
    :param label_col: The column containing the labels.
    :param timestamp_col: The column containing the timestamps.
    :return: A windowed DataFrame with the timestamp as index.
    """
    # Split DataFrame by label
    split_dfs = split_df(df, label_col)

    # Initialise list to store results
    res = []

    # Window over every DataFrame in the dfs list
    for df in split_dfs:
        # Determine label of DataFrame
        label = df[label_col].iloc[0]
        df_rolls = []

        # Determine index of timestamp 1 second after starting timestamp
        pivot = df[timestamp_col].iloc[0] + timedelta(seconds=1)
        cutoff = df.loc[df[timestamp_col] == nearest(df[timestamp_col].tolist(), pivot)]

        # Determine rows per second of DataFrame
        rps = cutoff.index[0] - df.index[0]

        for col in cols:
            # Get DataFrame with column and timestamp column
            df_col = df[[col, timestamp_col]]

            # Produce rolling object
            roll = df_col.rolling(window='2s', on=timestamp_col)

            # Apply built-in rolling functions

            # Mean
            df_roll = roll.mean()
            df_roll = df_roll.rename(columns={col: '%s_mean' % col})
            df_roll = df_roll[rps * 2 - 1::rps]
            df_rolls.append(df_roll)

            # Max
            df_roll = roll.max()
            df_roll = df_roll.rename(columns={col: '%s_max' % col})
            df_roll = df_roll[rps * 2 - 1::rps]
            df_rolls.append(df_roll)

            # Min
            df_roll = roll.min()
            df_roll = df_roll.rename(columns={col: '%s_min' % col})
            df_roll = df_roll[rps * 2 - 1::rps]
            df_rolls.append(df_roll)

            # Median
            df_roll = roll.median()
            df_roll = df_roll.rename(columns={col: '%s_median' % col})
            df_roll = df_roll[rps * 2 - 1::rps]
            df_rolls.append(df_roll)

            # Standard Deviation
            df_roll = roll.std()
            df_roll = df_roll.rename(columns={col: '%s_std' % col})
            df_roll = df_roll[rps * 2 - 1::rps]
            df_rolls.append(df_roll)

            # 25th Percentile
            df_roll = roll.quantile(.25)
            df_roll = df_roll.rename(columns={col: '%s_25_percentile' % col})
            df_roll = df_roll[rps * 2 - 1::rps]
            df_rolls.append(df_roll)

            # 75th Percentile
            df_roll = roll.quantile(.75)
            df_roll = df_roll.rename(columns={col: '%s_75_percentile' % col})
            df_roll = df_roll[rps * 2 - 1::rps]
            df_rolls.append(df_roll)

            # Kurtosis
            df_roll = roll.kurt()
            df_roll = df_roll.rename(columns={col: '%s_kurtosis' % col})
            df_roll = df_roll[rps * 2 - 1::rps]
            df_rolls.append(df_roll)

            # Skewness
            df_roll = roll.skew()
            df_roll = df_roll.rename(columns={col: '%s_skewness' % col})
            df_roll = df_roll[rps * 2 - 1::rps]
            df_rolls.append(df_roll)

        # Get timestamps from rolling
        timestamps = df_rolls[0][timestamp_col]

        # Drop timestamp column to prevent duplicates
        for df_roll in df_rolls:
            df_roll.drop(timestamp_col, axis=1, inplace=True)

        df_rolls = pd.concat(df_rolls, axis=1)
        df_rolls[label_col] = label
        df_rolls[timestamp_col] = timestamps

        res.append(df_rolls)

    # Concatenate DataFrames from list into one single DataFrame and return it
    return pd.concat(res).set_index(timestamp_col).sort_index(axis=1).sort_index(axis=0)

def split_df(df, col, temp):
    """
    Splits a data frame into multiple data frames based on the given column; if the column value
    changes, a new data frame is created. Changes are stored in the temp column, which has a
    False value for every new value in the given column. The temp column can be dropped after
    this function (is already done with the split data frames).
    :param df: The data frame that will be split up
    :param col: The column that determines the split locations
    :param temp: A temporary column name that can (should) be dropped after this function.
    :return: A list with the split data frames
    """
    # Create boolean column where every False signals a new value
    df[temp] = df[col].eq(df[col].shift())

    # Create a difference data frame with only the rows
    # of the changed values
    df_diff = df[df[temp] == 0]

    # Get the difference data frame index
    idx = df_diff.index.tolist()

    # Determine last index of original data frame
    last = df.index.tolist()[-1]

    result = []
    for i in range(len(idx) - 1):
        # Slice original data frame from changed value until the next
        new_df = df.loc[idx[i]:idx[i + 1] - 1]

        # Drop temporary column and add data frame to result list
        new_df = new_df.drop(temp, axis=1)
        result.append(new_df)

    # Slice the last part of the data frame, drop temporary column and
    # add it to the result list
    last_df = df.loc[idx[len(idx) - 1]:last]
    last_df = last_df.drop(temp, axis=1)
    result.append(last_df)
    return result


def windowing(df, col, size):
    if size > len(df):
        # Window size larger than data frame, so discard
        return

    # Roll (window) on data frame with function
    # TODO: allow for custom function
    new_df = df.rolling(window=size, on=col).mean()

    # Only take every <size>th row after rolling (cut off at len(df)/size rounded down)
    new_df = new_df[size - 1:: size]
    return new_df

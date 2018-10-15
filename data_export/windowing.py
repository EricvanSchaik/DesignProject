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


def windowing(df, col, step, offset=0):
    """
    Rolls over a data frame on a specific column with a given window size. An extra offset can be
    given to get overlap.

    :param df: Data frame that is getting rolled over.
    :param col: Specific column that is rolled on.
    :param step: Window size
    :param offset: Optional offset to get overlap
    :return: A windowed data frame
    """
    if step > len(df):
        # Window size larger than data frame, so discard
        return

    # Roll (window) on data frame with function
    # TODO: allow for custom function
    new_df = df.rolling(window=step, on=col).mean().fillna(df)

    # Only take every <step>th row after rolling (cut off at len(df)/step rounded down)
    df1 = new_df[step - 1::step]

    # If an extra offset is given, previous step is repeated with the extra offset to
    # get overlap, result is zipped together with previous result to get an end result.
    if offset > 0:
        df2 = new_df[step - 1 + offset::step]
        # Zip the partial data frames together to get the result
        return zip_df(df1, df2)

    # No extra offset given, so return first data frame only without zipping.
    return df1

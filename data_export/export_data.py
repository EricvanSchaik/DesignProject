def split_df(df, col, temp):
    df[temp] = df[col].eq(df[col].shift())
    df_diff = df[df[temp] == 0]

    idx = df_diff.index.tolist()
    last = df.index.tolist()[-1]

    result = []
    for i in range(len(idx) - 1):
        new_df = df.loc[idx[i]:idx[i + 1] - 1]
        result.append(new_df)
    last_df = df.loc[idx[len(idx) - 1]:last]
    result.append(last_df)
    return result

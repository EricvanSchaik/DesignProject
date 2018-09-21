def mul(x, args):
    # Args is a list of integers to be multiplied by each other and x
    for a in args:
        x *= a
    return x


def div(x, args):
    # Args is a list of one integer that divides x
    for a in args:
        x /= a
    return x


def add(x, args):
    # Args is a list of one integer that is subtracted from x
    for a in args:
        x += a
    return x


def sub(x, args):
    # Args is a list of integers to be added to each other and x
    for a in args:
        x -= a
    return x


def column_operation(df, col, func, *args):
    # Applies a function with arguments to a column of the data frame
    df[col] = df[col].apply(lambda x: func(x, args))

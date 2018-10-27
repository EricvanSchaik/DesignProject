import pandas as pd


def export(data: [], file_path: str, comments: [str], comment=';'):
    # Write comments to a file and use that as start file for 'to_csv'
    f = open(file_path, 'a')
    for c in comments:
        # TODO: determine whether '/n' needs to be added at end of line
        f.write(comment + c)

    # TODO: window over data

    # Turn list into one DataFrame
    df = pd.concat(data)

    # Write DataFrame to a csv file
    df.to_csv(f)

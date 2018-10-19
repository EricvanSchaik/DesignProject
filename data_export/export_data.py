import pandas as pd


def export(data: [], file_path, comment=';'):
    # TODO: write comments to a file and use that as start file for 'to_csv'

    # TODO: add segment number per data item

    # Turn list into one DataFrame
    df = pd.concat(data)

    # Write DataFrame to a csv file
    df.to_csv(file_path)

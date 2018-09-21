import re
import pandas as pd
from data_import import function as f


def parse_header(file_path):
    # create list of headers
    headers = []

    # Add headers to header list
    with open(file_path) as file:
        for line in file:
            if line.startswith(";"):
                # semicolon at start of line indicates a comment, ergo a header
                # remove it and convert line from string to list of arguments
                headers.append(re.split(', *', line[1:-1]))
            else:
                # end of header section
                break
    return headers


def parse_csv(file_path):
    # create list of headers
    headers = parse_header(file_path)

    # Get names of columns
    names = get_names(headers)

    # Parse data
    data = pd.read_csv(file_path, header=None, names=names, comment=';')

    # Convert sensor data to correct unit
    # Accelerometer to m/s
    f.column_operation(data, names[1], f.mul, 9.807 / 4096)
    f.column_operation(data, names[2], f.mul, 9.807 / 4096)
    f.column_operation(data, names[3], f.mul, 9.807 / 4096)

    # Gyroscope data to ?/s
    f.column_operation(data, names[4], f.div, 16.384)
    f.column_operation(data, names[5], f.div, 16.384)
    f.column_operation(data, names[6], f.div, 16.384)

    # Magnetometer to ?T (micro Tesla)
    f.column_operation(data, names[7], f.div, 3.413)
    f.column_operation(data, names[8], f.div, 3.413)
    f.column_operation(data, names[9], f.div, 3.413)

    # Return data
    return data


def get_header(headers, prefix):
    # find header with given prefix
    for h in headers:
        if h[0].lower() == prefix.lower():
            return h[1:]
    return -1


def get_names(headers):
    # last header is list of column names
    if len(headers) < 1:
        return -1
    return headers[-1]


print(parse_csv("../data/DATA-001.CSV").head())

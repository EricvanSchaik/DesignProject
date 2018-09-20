import re
import pandas as pd


def parse_csv(file_path):
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

    # Get names of columns
    names = get_names(headers)

    # Parse data
    data = pd.read_csv(file_path, header=None, names=names, comment=';')

    # for h in headers:
    #     print(h)
    # print(data)
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


print(parse_csv("../data/DATA-001.CSV"))

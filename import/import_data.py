import re


def parse(file_path):
    # Open file from path
    file = open(file_path)

    # split file into headers and data
    headers = []
    data = []
    for line in file:
        if line.startswith(";"):
            # remove semicolon ';' from front of header and convert from string to list
            headers.append(re.split(', *', line[1:-1]))
        else:
            # convert data from string to list
            data.append(line[:-1].split(","))

    # get list of variable names
    names = get_variable_names(headers)
    for h in headers:
        print(h)
    pass


def get_start_time(headers):
    # find header with start_time prefix
    for h in headers:
        if h[0].lower() == "start_time":
            return h[1:]
    return -1


def get_variable_names(headers):
    # last header is list of variable names
    if len(headers) < 1:
        return -1
    return headers[-1]


parse("../data/DATA-001.CSV")

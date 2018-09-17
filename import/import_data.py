def parse(file_path):
    # Open file from path
    file = open(file_path)

    # split file into headers and data
    headers = []
    data = []
    for line in file:
        if line.startswith(";"):
            # remove semicolon ';' from front of header and convert from string to list
            headers.append(line[1:-1].split(","))
        else:
            # convert data from string to list
            data.append(line[:-1].split(","))

    # create list of variable names
    names = find_variable_names(headers)
    print(names)
    pass


def find_start_time(headers):
    pass


def find_variable_names(headers):
    if len(headers) < 1:
        return -1
    return headers[-1]


parse("../data/DATA-001.CSV")

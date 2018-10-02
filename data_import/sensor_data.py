import re
import pandas as pd
from data_import import sensor as sens, column_metadata as cm
import parse_string.custom_function_parser as parser
from parse_string.parse_exception import ParseException


def parse_header_option(file, row_nr, col_nr):
    """
    Parses a specific part of the header with a line number and a column number
    :param file: file to be parsed
    :param row_nr: row number of header
    :param col_nr: column number of header data
    :return: data on row and column number or -1 if the file is smaller than the row number
    """
    # return to start of file
    file.seek(0)

    i = 1  # row numbers start at 1
    for line in file:
        if i == row_nr:
            return re.split(', *', line)[col_nr - 1]  # column numbers start at 1
        else:
            i += 1
    # error
    return -1


def parse_names(file, row_nr):
    """
    Parses the names of the data columns using a row number
    :param file: file to be parsed
    :param row_nr: row number of names
    :return: list of column names or -1 if the file is smaller than the row number
    """
    # return to start of file
    file.seek(0)

    i = 1
    for line in file:
        if i == row_nr:
            return re.split(', *', line[1:-1])
        else:
            i += 1
    # error
    return -1


class SensorData:

    def __init__(self, file_path, settings):
        """
        The SensorData starts parsing as soon as it's constructed. Only SensorData.data needs to
        be called in order to get the parsed data. SensorData.metadata contains the metadata.
        :param file_path: path to the file to be parsed
        :param settings: The settings dictionary contains information on where metadata can
        be found in the parsed file. It should have the following keys in order for it to work:

            - time_row, time_col   (row and column where 'time' attribute is located)
            - date_row, date_col   (row and column where 'date' attribute is located)
            - sr_row, sr_col       (row and column where 'sampling rate' attribute is located)
            - sn_row, sn_col       (row and column where 'serial number' attribute is located)
            - names_row            (row where the names of the columns are located)

            - comment              (symbol used to indicate a comment !this is a value, not a location!)

        The next keys are variable depending on the name of the column (these are not locations, but values!):

            - <name>_data_type     (data type of the column)
            - <name>_sensor_name   (name of the sensor used)
            - <name>_sampling_rate (sampling rate of the sensor)
            - <name>_unit          (unit of measurement of the sensor)
            - <name>_conversion    (conversion function for the data)
        """
        # Initiate primitives
        self.file_path = file_path
        self.metadata = dict()
        self.col_metadata = dict()

        # Parse metadata and data
        self.data = self.parse(settings)

    def parse(self, settings):
        """
        Parses a csv file to get metadata and data.
        :param settings: contains the metadata
        :return: the parsed data
        """
        # Parse metadata from headers
        with open(self.file_path) as file:
            self.metadata['time'] = parse_header_option(file, settings['time_row'], settings['time_col'])
            self.metadata['date'] = parse_header_option(file, settings['date_row'], settings['date_col'])
            self.metadata['sr'] = parse_header_option(file, settings['sr_row'], settings['sr_col'])
            self.metadata['sn'] = parse_header_option(file, settings['sn_row'], settings['sn_col'])
            self.metadata['names'] = parse_names(file, settings['names_row'])

        # set column metadata
        self.set_column_metadata(settings)

        # Parse data from file
        data = pd.read_csv(self.file_path, header=None, names=self.metadata['names'],
                           comment=settings['comment'])

        # Pass parse exceptions on
        try:
            # Convert sensor data to correct unit
            for name in self.metadata['names']:
                # Retrieve conversion rate from column metadata
                conversion = self.col_metadata[name].sensor.conversion

                # If column doesn't have a conversion, continue to next column
                if conversion is None:
                    continue

                # Parse conversion to python readable expression
                parsed_expr = parser.parse(conversion)

                # Apply parsed expression to the data
                data.eval(name + " = " + parsed_expr, inplace=True)
        except ParseException:
            # Pass parse exception
            raise
        return data

    def set_column_metadata(self, settings):
        """
        Sets the metadata for every column using the settings
        """
        for name in self.metadata['names']:
            # parse data_type
            data_type = (settings[name + "_data_type"]
                         if name + "_data_type" in settings.keys() else None)

            # parse sensor:
            # sensor name
            sensor_name = (settings[name + "_sensor_name"]
                           if name + "_sensor_name" in settings.keys() else None)

            # sampling rate
            sr = (settings[name + "_sampling_rate"]
                  if name + "_sampling_rate" in settings.keys() else None)

            # unit of measurement
            unit = (settings[name + "_unit"]
                    if name + "unit" in settings.keys() else None)

            # conversion rate
            conversion = (settings[name + "_conversion"]
                          if name + "_conversion" in settings.keys() else None)

            # construct sensor
            sensor = sens.Sensor(sensor_name, sr, unit, conversion)

            # create new column metadata and add it to list with metadata
            self.col_metadata[name] = cm.ColumnMetadata(name, data_type, sensor)

    def add_column(self, name: str, func: str):
        """
        Constructs a new column in the data frame using a given function
        :param name: The name of the new column
        :param func: The function to calculate the values of the new column as a string
        """
        # Pass parse exception on
        try:
            # Parses a function into a python readable expression
            parsed_expr = parser.parse(func)

            # Apply parsed expression to data to create new column
            self.data.eval(name + " = " + parsed_expr, inplace=True)
        except ParseException:
            # Pass parse exception
            raise

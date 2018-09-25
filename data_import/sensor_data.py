import re
import pandas as pd
from data_import import sensor as sens, column_metadata as cm


def parse_header_option(file, row_nr, col_nr):
    """
    Parses a specific part of the header with a line number and a column number
    :param file: file to be parsed
    :param row_nr: row number of header
    :param col_nr: column number of header data
    :return: data on row and column number
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
    :return: list of column names
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
        """
        # Initiate primitives
        self.file_path = file_path
        self.metadata = dict()
        self.names = []
        self.col_metadata = dict()

        # Parse metadata and data
        self.data = self.parse(settings)

    def parse(self, settings):
        """
        Parses a csv file to get metadata and data.
        :param settings: contains the metadata
        :return: the data
        """
        # Parse metadata from headers
        with open(self.file_path) as file:
            self.metadata['time'] = parse_header_option(file, settings['time_row'], settings['time_col'])
            self.metadata['date'] = parse_header_option(file, settings['date_row'], settings['date_col'])
            self.metadata['sr'] = parse_header_option(file, settings['sr_row'], settings['sr_col'])
            self.metadata['sn'] = parse_header_option(file, settings['sn_row'], settings['sn_col'])
            self.names = parse_names(file, settings['names_row'])

        # set column metadata
        self.set_column_metadata(settings)

        # Parse data from file
        data = pd.read_csv(self.file_path, header=None, names=self.names, comment=settings['comment'])

        # Convert sensor data to correct unit
        for name in self.names:
            conversion = self.col_metadata[name].sensor.conversion

            # If column doesn't have a conversion, continue to next column
            if conversion is None:
                continue

            # Apply conversion to the data
            data[name] = data[name].apply(lambda x: x * conversion)

        return data

    def set_column_metadata(self, settings):
        """
        Sets the metadata for every column using the settings
        """
        for name in self.names:
            # parse data_type
            data_type = settings[name + "_data_type"]

            # parse sensor:
            # sensor name
            sensor_name = settings[name + "_sensor_name"]

            # sampling rate
            sr = settings[name + "_sampling_rate"]

            # unit of measurement
            unit = settings[name + "_unit"]

            # TODO: parse conversion rate automatically with a given function
            conversion = None
            if name.startswith("A"):  # Accelerometer
                conversion = 9.807 / 4096
            elif name.startswith("G"):  # Gyroscope
                conversion = 1 / 16.384
            elif name.startswith("M"):  # Magnetometer
                conversion = 1 / 3.413
            elif name == "T":  # Temperature
                conversion = 1 / 1000

            # construct sensor
            sensor = sens.Sensor(sensor_name, sr, unit, conversion)

            # create new column metadata and add it to list with metadata
            self.col_metadata[name] = cm.ColumnMetadata(name, data_type, sensor)

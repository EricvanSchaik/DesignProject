import re
import pandas as pd
from data_import import function as f


class Sensor:

    def __init__(self, file_path):
        self.file_path = file_path
        self.headers = self.parse_headers()
        self.data = self.parse_data()

    def parse_headers(self):
        """
        Parses a csv file to get the headers. Ignores the data.
        :return: a 2D list with information on the sensor and its data.
        """

        # create list of headers
        headers = []

        # Add headers to header list
        with open(self.file_path) as file:
            for line in file:
                if line.startswith(";"):
                    # semicolon at start of line indicates a comment, ergo a header
                    # remove it and convert line from string to list of arguments
                    headers.append(re.split(', *', line[1:-1]))
                else:
                    # end of header section
                    break
        return headers

    def parse_data(self):
        """
        Parses a csv file to get its data. Ignores the headers
        :return: a DataFrame with this sensor's data
        """
        # Get names of columns
        names = self.get_names()

        # Parse data
        data = pd.read_csv(self.file_path, header=None, names=names, comment=';')

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

        # Temperature to C
        f.column_operation(data, names[10], f.div, 1000)

        # Return data
        return data

    def get_names(self):
        """
        Retrieves the names of the columns
        :return: names of the columns
        """
        if len(self.headers) < 1:
            return -1
        return self.headers[-1]

    def get_header(self, prefix):
        """
        Finds the header with the given prefix.
        :param prefix: prefix of the header
        :return: the header corresponding to the prefix
        """
        for h in self.headers:
            if h[0].lower() == prefix.lower():
                return h[1:]
        return -1

    def get_time(self):
        """
        Retrieves the date and start time of the sensor.
        :return: List containing the date and start time of the sensor
        """
        return self.get_header('Start_time')

    def get_serial_number(self):
        """
        Retrieves the serial number of the sensor.
        :return: Serial Number of used sensor
        """
        return self.get_header('Version')[3]

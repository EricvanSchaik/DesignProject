import unittest
from data_export import windowing_test as wt
from data_export import export_data as ed
import os


class ExportDataTestCase(unittest.TestCase):

    def setUp(self):
        df = wt.test_sensor_data()
        self.dfs = [df.head(1000), df.iloc[1000:2000], df.iloc[2000:3000], df.tail(1000)]

    def test_export(self):
        file_path = '../data/export_unit_test.csv'
        ed.export(self.dfs, 'Label', 'Timestamp', file_path, [])

        # TODO: add assertions

        # Remove file after test
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print('%s does not exist' % file_path)

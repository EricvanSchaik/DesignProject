import unittest
from data_import import sensor_data as sd


def create_settings():
    settings = dict()
    settings['time_row'], settings['time_col'] = 3, 3
    settings['date_row'], settings['date_col'] = 3, 2
    settings['sr_row'], settings['sr_col'] = 5, 2
    settings['sn_row'], settings['sn_col'] = 2, 5
    settings['names_row'] = 8
    settings['comment'] = ';'

    names = ["Time", "Ax", "Ay", "Az", "Gx", "Gy", "Gz", "Mx", "My", "Mz", "T"]
    for name in names:
        settings[name + "_data_type"] = "-"
        settings[name + "_sensor_name"] = "-"
        settings[name + "_sampling_rate"] = "-"
        settings[name + "_unit"] = "-"

    settings["Ax_conversion"] = 9.807 / 4096
    settings["Ay_conversion"] = 9.807 / 4096
    settings["Az_conversion"] = 9.807 / 4096

    settings["Gx_conversion"] = 1 / 16.384
    settings["Gy_conversion"] = 1 / 16.384
    settings["Gz_conversion"] = 1 / 16.384

    settings["Mx_conversion"] = 1 / 3.413
    settings["My_conversion"] = 1 / 3.413
    settings["Mz_conversion"] = 1 / 3.413

    settings["T_conversion"] = 1 / 1000

    return settings


class SensorDataTestCase(unittest.TestCase):

    def setUp(self):
        self.sensor_data = sd.SensorData("../data/DATA-001.CSV", create_settings())

    def test_add_column(self):
        self.sensor_data.add_column("Vector", sd.vector)
        self.assertEqual(self.sensor_data.data["Vector"][0], 8.536469993305431,
                         "Vector incorrectly calculated")

    def test_metadata(self):
        self.assertEqual(self.sensor_data.metadata['time'], "08:54:32.261\n",
                         "Parsed time incorrectly")
        self.assertEqual(self.sensor_data.metadata['date'], "2018-05-15",
                         "Parsed date incorrectly")
        self.assertEqual(self.sensor_data.metadata['sr'], "200",
                         "Parsed sampling rate incorrectly")
        self.assertEqual(self.sensor_data.metadata['sn'], "SN:CCDC3016AE9D6B4\n",
                         "Parsed serial number incorrectly")
        self.assertEqual(self.sensor_data.metadata['names'][1], "Ax",
                         "Parsed names incorrectly")

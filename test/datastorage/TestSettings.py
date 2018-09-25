import unittest
from datastorage.Settings import *


class TestSettings(unittest.TestCase):

    def setUp(self):
        Settings('test_project', True)

    def tearDown(self):
        os.remove('projects/test_project/' + settings_file_name)

    def test_get_set_setting(self):
        s1 = Settings('test_project')
        self.assertIs(None, s1.get_setting('test_setting1'))  # setting 'test_setting1' should not be set yet
        s1.set_setting('test_setting1', 'test_value')         # set the value of 'test_setting1' to 'test_value'

        s2 = Settings('test_project')                                    # create a new Settings instance
        self.assertEqual('test_value', s2.get_setting('test_setting1'))  # 'test_setting1' should return 'test_value'
        s2.set_setting('test_setting2', 42)
        self.assertEqual(42, s2.get_setting('test_setting2'))  # integer values should also work

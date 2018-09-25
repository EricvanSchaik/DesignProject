import unittest
from datastorage.SubjectMapping import *


class TestSubjects(unittest.TestCase):

    s = SubjectManager('test_project')

    def setUp(self):
        self.s.create_table()

    def tearDown(self):
        self.s._cur.execute('DROP TABLE subject_map')

    def test_add_subject(self):
        self.s.add_subject('subject')
        self.assertEqual('subject', self.s._cur.execute('SELECT Name FROM subject_map').fetchone()[0])

    def test_change_subject_info(self):
        self.s.add_subject('subject')
        self.s.change_sensor('subject', 'sensor1')
        self.assertEqual('sensor1', self.s._cur.execute('SELECT Sensor FROM subject_map').fetchone()[0])
        self.s.change_start_date('subject', '2018-09-10')
        self.assertEqual('2018-09-10', self.s._cur.execute('SELECT Start_date FROM subject_map').fetchone()[0])
        self.s.change_end_date('subject', '2018-09-25')
        self.assertEqual('2018-09-25', self.s._cur.execute('SELECT End_date FROM subject_map').fetchone()[0])

import unittest
from datastorage.labelstorage import *


class TestLabels(unittest.TestCase):

    l = LabelManager('test_project')

    def setUp(self):
        self.l.create_tables()

    def tearDown(self):
        self.l._cur.execute('DROP TABLE labelType')
        self.l._cur.execute('DROP TABLE labelData')

    def test_add_del_label_type(self):
        self.l.add_label_type('label1', 420, 'This is a test label')     # add new label type with name 'label1'
        self.assertNotEqual(0, len(
            self.l._cur.execute('SELECT * FROM labelType').fetchall()))  # new label type should be in the table
        self.l.add_label(datetime.now(), datetime.now(), 'label1', 'sensor1')  # create a label with the new type
        self.l.delete_label_type('label1')
        self.assertEqual(0, len(
            self.l._cur.execute('SELECT * FROM labelType').fetchall()))  # label type should not be in the table
        self.assertEqual(0, len(
            self.l._cur.execute('SELECT * FROM labelData').fetchall()))  # label should not be in the table

    def test_add_del_label(self):
        label_time = datetime.now()
        self.l.add_label(label_time, label_time, 'label1', 'sensor1')    # add new label at time 1.5 to sensor 'sensor1'
        self.assertNotEqual(0, len(
            self.l._cur.execute('SELECT * FROM labelData').fetchall()))  # new label should be in the table
        self.l.delete_label(label_time, 'sensor1')
        self.assertEqual(0, len(
            self.l._cur.execute('SELECT * FROM labelData').fetchall()))  # label should not be in the table

    def test_update_label_type(self):
        label_time = datetime.now()
        self.l.add_label_type('label1', 420, 'This is a test label')   # add new label type with name 'label1'
        self.l.add_label(label_time, label_time, 'label1', 'sensor1')  # create a label with the new type
        self.assertEqual('label1', self.l._cur.execute('SELECT Name FROM labelType')
                         .fetchone()[0])  # label type name should be 'label1'
        self.assertEqual(420, self.l._cur.execute('SELECT Color FROM labelType')
                         .fetchone()[0])  # label type color should be 420
        self.assertEqual('This is a test label', self.l._cur.execute('SELECT Description FROM labelType')
                         .fetchone()[0])  # label type description should be 'This is a test label'
        self.l.update_label_color('label1', 42)
        self.assertEqual(42, self.l._cur.execute('SELECT Color FROM labelType')
                         .fetchone()[0])  # label type color should now be 420
        self.l.update_label_description('label1', 'This is a changed description')
        self.assertEqual('This is a changed description', self.l._cur.execute('SELECT Description FROM labelType')
                         .fetchone()[0])  # label type description should now be 'This is a changed description'
        self.l.update_label_name('label1', 'label2')
        self.assertEqual('label2', self.l._cur.execute('SELECT Name FROM labelType')
                         .fetchone()[0])  # label type name should now be 'label2'
        self.assertEqual('label2', self.l._cur.execute('SELECT Label_name FROM labelData')
                         .fetchone()[0])  # label created with the label type should also be named 'label2' now

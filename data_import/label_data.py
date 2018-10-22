import csv

from datastorage.labelstorage import LabelManager
from datetime import datetime


class LabelData:
    """
    This class can be used to retrieve and update labels from the database.
    """

    START_TIME_INDEX = 0
    STOP_TIME_INDEX = 1
    LABEL_INDEX = 2

    def __init__(self, sensor_id: str, label_manager: LabelManager):
        self._sensor_id = sensor_id
        self._label_manager = label_manager
        self._data = self.fill_from_db()

    def fill_from_db(self):
        return self._label_manager.get_all_labels(self._sensor_id)

    def get_data(self):
        return self._data

    def get_sensor_id(self):
        return self._sensor_id

    def set_sensor_id(self, sensor_id: str):
        self._sensor_id = sensor_id

    def add_data(self, labels: [[]]):
        """
        Adds a list of labels to the database.

        :param labels: A list of labels to put in the database
        """
        for label in labels:
            self._label_manager.add_label(label[self.START_TIME_INDEX], label[self.STOP_TIME_INDEX],
                                          label[self.LABEL_INDEX], self._sensor_id)
        self._data = self.fill_from_db()


if __name__ == '__main__':
    labels_file = open('data/20180515_09-58_CCDC301661B33D7_labels.csv')
    project_name = 'test_project'
    sensor_id = 'CCDC301661B33D7'

    lbm = LabelManager(project_name)
    lbd = LabelData(sensor_id, lbm)

    # Set up label file reader
    labels = csv.reader(labels_file)
    next(labels)
    labels = sorted(labels, key=lambda row: row[0])

    res = []

    # Add a stop time to the rows
    for i in range(len(labels) - 1):
        res.append([datetime.strptime(labels[i][0], "%Y%m%d %H:%M:%S.%f"), datetime.strptime(labels[i + 1][0], "%Y%m%d %H:%M:%S.%f"), labels[i][1]])

    lbd.add_data(res)
    print(lbd.get_data())

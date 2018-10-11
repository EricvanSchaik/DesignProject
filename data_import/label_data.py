import datetime as dt

from datastorage.labelstorage import LabelManager


class LabelData:

    def __init__(self, sensor_id: str, label_manager: LabelManager):
        self._sensor_id = sensor_id
        self._label_manager = label_manager
        self._labels = self.fill_from_db()

    def fill_from_db(self):
        return self._label_manager.get_all_labels(self._sensor_id)

    def get_labels(self):
        return self._labels

    def get_sensor_id(self):
        return self._sensor_id

    def set_sensor_id(self, sensor_id: str):
        self._sensor_id = sensor_id

    def add_label(self, start_time: dt.datetime, stop_time: dt.datetime, label: str):
        self._label_manager.add_label(start_time, stop_time, label, self._sensor_id)


if __name__ == '__main__':
    project_name = 'test_project'
    sensor_id = 'SN:CCDC3016AE9D6B4'
    lbm = LabelManager(project_name)
    lbd = LabelData(sensor_id, lbm)

    print(lbd.get_labels())

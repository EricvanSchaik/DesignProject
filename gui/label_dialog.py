from PyQt5 import QtWidgets

from datastorage.labelstorage import LabelManager
from gui.designer_labelspecs import Ui_LabelSpecs
from datetime import datetime


class LabelSpecs(QtWidgets.QDialog, Ui_LabelSpecs):

    def __init__(self, project_name, serial_number, start_time=0):
        super().__init__()
        # Initialize the generated UI from designer_gui.py.
        self.setupUi(self)

        self.serial_number = serial_number
        self.start_time = start_time
        self.label = Label()
        self.doubleSpinBox_start.valueChanged.connect(self.start_changed)
        self.doubleSpinBox_end.valueChanged.connect(self.stop_changed)
        self.label_manager = LabelManager(project_name)
        self.accepted.connect(self.send_label)
        self.comboBox_labels.activated.connect(self.label_changed)

    def start_changed(self, value: float):
        self.label.start = value + self.start_time

    def stop_changed(self, value: float):
        self.label.end = value + self.start_time

    def label_changed(self, label: str):
        self.label.label = label

    def send_label(self):
        print(self.label_manager.get_all_labels(self.serial_number))
        # self.label_manager.add_label(datetime.fromtimestamp(self.label.start), datetime.fromtimestamp(
        #     self.label.end), str(self.label.label), self.serial_number)


class Label:

    def __init__(self):
        self.label = 0
        self.start = 0.00
        self.end = 0.00

    def setLabel(self, name: str):
        self.label = name

    def setStart(self, start: float):
        self.start = start

    def setEnd(self, end: float):
        self.end = end

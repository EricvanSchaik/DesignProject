from PyQt5 import QtWidgets

from datastorage.labelstorage import LabelManager
from gui.designer_labelspecs import Ui_LabelSpecs


class LabelSpecs(QtWidgets.QDialog, Ui_LabelSpecs):

    def __init__(self, project_name):
        super().__init__()
        # Initialize the generated UI from designer_gui.py.
        self.setupUi(self)
        self.label = Label()
        self.doubleSpinBox_start.valueChanged.connect(self.start_changed)
        self.doubleSpinBox_end.valueChanged.connect(self.stop_changed)
        self.label_storage = LabelManager(project_name)
        self.accepted.connect(self.send_label)
        self.comboBox_labels.activated.connect(self.label_changed)

    def start_changed(self, value: float):
        self.label.start = value

    def stop_changed(self, value: float):
        self.label.stop = value

    def label_changed(self, label: str):
        self.label.label = label

    def send_label(self):
        self.label_storage.add_label(self.label.start, self.label.end, self.label.label, "")


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

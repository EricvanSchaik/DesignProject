from PyQt5 import QtWidgets

from gui.designer_labelsettings import Ui_Dialog
from datastorage.labelstorage import LabelManager


class LabelSettingsDialog(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, label_manager: LabelManager):
        super().__init__()
        self.setupUi(self)
        self.label_manager = label_manager
        self.lineEdit.returnPressed.connect(self.add_label)
        self.pushButton.clicked.connect(self.delete_label)
        self.comboBox.currentTextChanged.connect(self.label_changed)
        colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white']
        self.comboBox_2.addItems(colors)
        self.comboBox_3.addItems(colors)
        self.color_dict = dict()
        for label in self.label_manager.get_label_types():
            self.comboBox.addItem(label[0])
            self.color_dict[label[0]] = label[1]
        if self.label_manager.get_label_types():
            self.comboBox_2.setCurrentText(self.label_manager.get_label_types()[0][1])

    def add_label(self):
        self.label_manager.add_label_type(self.lineEdit.text(), self.comboBox_3.currentText(), '')
        for label in self.label_manager.get_label_types():
            self.comboBox.addItem(label[0])
            self.color_dict[label[0]] = label[1]
        self.comboBox_2.setCurrentText(self.label_manager.get_label_types()[0][1])
        self.lineEdit.clear()

    def delete_label(self):
        pass

    def label_changed(self, text):
        if self.color_dict:
            self.comboBox_2.setCurrentText(self.color_dict[text])

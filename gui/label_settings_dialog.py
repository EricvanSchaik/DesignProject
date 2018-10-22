from PyQt5 import QtWidgets

from gui.designer_labelsettings import Ui_Dialog
from datastorage.labelstorage import LabelManager


class LabelSettingsDialog(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, label_manager: LabelManager):
        super().__init__()
        self.setupUi(self)
        self.label_manager = label_manager
        self.accepted.connect(self.add_label)
        self.pushButton.clicked.connect(self.delete_label)
        self.comboBox.currentTextChanged.connect(self.label_changed)
        self.comboBox_2.currentTextChanged.connect(self.color_changed)
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
        if self.lineEdit.text():
            self.label_manager.add_label_type(self.lineEdit.text(), self.comboBox_3.currentText(), '')

    def delete_label(self):
        self.label_manager.delete_label_type(self.comboBox.currentText())
        self.comboBox.clear()
        for label in self.label_manager.get_label_types():
            self.comboBox.addItem(label[0])
            self.color_dict[label[0]] = label[1]
        if self.label_manager.get_label_types():
            self.comboBox_2.setCurrentText(self.label_manager.get_label_types()[0][1])

    def label_changed(self, text):
        if self.color_dict and self.comboBox.count():
            self.comboBox_2.setCurrentText(self.color_dict[text])

    def color_changed(self, color):
        if self.comboBox.currentText():
            self.label_manager.update_label_color(self.comboBox.currentText(), color)
            self.color_dict[self.comboBox.currentText()] = color

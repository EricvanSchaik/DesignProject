from PyQt5 import QtWidgets

from gui.designer_labelsettings import Ui_Dialog
from datastorage.labelstorage import LabelManager


class LabelSettingsDialog(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, label_manager: LabelManager):
        super().__init__()
        self.setupUi(self)
        self.label_manager = label_manager
        self.lineEdit.returnPressed.connect(self.add_label)
        colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white']
        self.comboBox_2.addItems(colors)
        self.comboBox_3.addItems(colors)
        for label in self.label_manager.get_label_types():
            self.comboBox.addItem(label[0])

    def add_label(self):
        self.label_manager.add_label_type(self.lineEdit.text(), self.comboBox_3.itemText(0), '')

from PyQt5 import QtWidgets
from gui.designer_machine_learning import Ui_Dialog


class MachineLearningDialog(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, columns):
        super().__init__()
        self.setupUi(self)
        self.is_accepted = False
        self.column_dict = dict()
        for column in columns:
            self.column_dict[column] = False
        self.accepted.connect(self.activate)
        self.radioButton.toggled.connect(self.switch)
        self.checkBox.toggled.connect(self.add_column)
        self.comboBox.currentTextChanged.connect(self.switch_column)
        self.comboBox.setEnabled(False)
        self.checkBox.setEnabled(False)
        self.comboBox.addItems(columns)

    def activate(self):
        self.is_accepted = True

    def switch(self, event):
        if event:
            self.comboBox.setEnabled(True)
            self.checkBox.setEnabled(True)
        else:
            self.comboBox.setEnabled(False)
            self.checkBox.setEnabled(False)

    def add_column(self, event):
        self.column_dict[self.comboBox.currentText()] = event

    def switch_column(self):
        self.checkBox.setChecked(self.column_dict[self.comboBox.currentText()])

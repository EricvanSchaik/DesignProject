from PyQt5 import QtWidgets

from gui.designer_labelsettings import Ui_Dialog

class LabelSettingsDialog(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

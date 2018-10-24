from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QTableWidgetItem, QMessageBox

from gui.designer_subject_table import Ui_Subject_table
from datastorage.subjectmapping import SubjectManager


class SubjectTable(QtWidgets.QDialog, Ui_Subject_table):

    def __init__(self, project_name: str):
        super().__init__()
        # Initialize the generated UI from designer_gui.py.
        self.setupUi(self)

        self.project_name = project_name
        self.subject_manager = SubjectManager(project_name)
        self.col_names, self.table_data = self.subject_manager.get_table()
        self.subject_names = [x[0] for x in self.table_data]
        print(self.subject_names)
        self.tableWidget.setColumnCount(len(self.col_names))

        # self.accepted.connect()
        self.rowButton.clicked.connect(self.add_row)
        self.colButton.clicked.connect(self.add_col)
        self.print.clicked.connect(self.print_00)

        self.tableWidget.cellChanged.connect(self.update_cell)

    def add_row(self):
        text, accepted = QInputDialog.getText(self, "Enter new subject name", "Subject name:", QLineEdit.Normal, "")
        if accepted:
            if text == '':
                QMessageBox.warning(self, 'Warning', "Give a subject name", QMessageBox.Cancel)
                return
            if text in self.subject_names:
                QMessageBox.warning(self, 'Warning', "The name of this subject already exists", QMessageBox.Cancel)
                return
            self.tableWidget.blockSignals(True)
            position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(position)
            self.tableWidget.setItem(position, 0, QTableWidgetItem(text))
            self.tableWidget.blockSignals(False)

    def add_col(self):
        self.tableWidget.insertColumn(self.tableWidget.columnCount())

    def print_00(self):
        pass

    def update_cell(self):
        x = self.tableWidget.currentRow()
        y = self.tableWidget.currentColumn()
        print("{},{}".format(x, y))
        value = self.tableWidget.item(x, y).text()
        print("value: " + value)

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QTableWidgetItem

from gui.designer_subject_table import Ui_Subject_table
from datastorage.subjectmapping import SubjectManager


class SubjectTable(QtWidgets.QDialog, Ui_Subject_table):

    def __init__(self, project_name: str):
        super().__init__()
        # Initialize the generated UI from designer_gui.py.
        self.setupUi(self)

        self.project_name = project_name
        self.subject_manager = SubjectManager(project_name)
        self.row_count = 0

        # self.accepted.connect()
        self.rowButton.clicked.connect(self.add_row)
        self.colButton.clicked.connect(self.add_col)
        self.print.clicked.connect(self.print_00)

        self.tableWidget.cellChanged.connect(self.update_cell)

    def add_row(self):
        text, okPressed = QInputDialog.getText(self, "Enter new subject name", "Subject name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
        self.tableWidget.insertRow(self.tableWidget.rowCount())


    def add_col(self):
        self.tableWidget.insertColumn(self.tableWidget.columnCount())

    def print_00(self):
        new_item = QTableWidgetItem()
        new_item.setText("test123321")
        print(new_item.text())
        self.tableWidget.setCellWidget(0, 0, new_item)

    def update_cell(self):
        x = self.tableWidget.currentRow()
        y = self.tableWidget.currentColumn()
        print("{},{}".format(x, y))
        value = self.tableWidget.item(x, y).text()
        print("value: " + value)

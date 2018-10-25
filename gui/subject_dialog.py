from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QTableWidgetItem, QMessageBox, QDateEdit

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
        self.tableWidget.setColumnCount(len(self.col_names))
        self.tableWidget.setRowCount(len(self.table_data))

        self.tableWidget.setHorizontalHeaderLabels(self.col_names)
        # fill table
        self.tableWidget.blockSignals(True)
        for i in range(len(self.table_data)):
            for j in range(len(self.table_data[i])):
                item = self.table_data[i][j]
                # TODO: get sensor IDs from database and use drop-down menu
                if j == 2 or j == 3:
                    date_item = QDateEdit(QDate(item.year, item.month, item.day))
                    date_item.dateChanged.connect(self.update_date)
                    self.tableWidget.setCellWidget(i, j, date_item)
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(item))
        self.tableWidget.blockSignals(False)

        self.closeButton.clicked.connect(self.close)
        self.rowButton.clicked.connect(self.add_row)
        self.colButton.clicked.connect(self.add_col)
        self.delSubjectButton.clicked.connect(self.delete_row)
        self.delColumnButton.clicked.connect(self.delete_column)

        self.tableWidget.cellChanged.connect(self.update_string)

    def add_row(self):
        text, accepted = QInputDialog.getText(self, "Enter new subject name", "Subject name:", QLineEdit.Normal, "")
        if accepted:
            if text == '':
                self.show_warning("Give a subject name")
                return
            if text in self.subject_names:
                self.show_warning("The name of this subject already exists")
                return
            self.tableWidget.blockSignals(True)
            position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(position)
            self.tableWidget.setItem(position, 0, QTableWidgetItem(text))
            self.subject_names += [text]
            self.subject_manager.add_subject(text)

            start_date = QDateEdit(QDate.currentDate())
            start_date.dateChanged.connect(self.update_date)
            end_date = QDateEdit(QDate.currentDate())
            end_date.dateChanged.connect(self.update_date)
            self.subject_manager.update_start_date(text, datetime.now())
            self.subject_manager.update_end_date(text, datetime.now())
            self.tableWidget.setCellWidget(position, 2, start_date)
            self.tableWidget.setCellWidget(position, 3, end_date)

            self.tableWidget.blockSignals(False)

    def add_col(self):
        text, accepted = QInputDialog.getText(self, "Enter new column name", "Column name:", QLineEdit.Normal, "")
        if accepted:
            if text == '':
                self.show_warning("Give a column name")
                return
            if text in self.col_names:
                self.show_warning("The name of this column already exists")
                return
            position = self.tableWidget.columnCount()
            self.tableWidget.insertColumn(position)
            self.tableWidget.setHorizontalHeaderItem(position, QTableWidgetItem(text))
            self.subject_manager.add_column(text)
            self.col_names += [text]

    def delete_row(self):
        subject, accepted = QInputDialog.getItem(self, "Select a subject",
                                                 "Select a subject to remove", self.subject_names, 0, False)
        if accepted:
            self.subject_manager.delete_subject(subject)
            row = self.subject_names.index(subject)
            self.subject_names.remove(subject)
            self.tableWidget.removeRow(row)

    def delete_column(self):
        if len(self.col_names) == 4:
            self.show_warning("There is no column that can be deleted")
            return

        col_name, accepted = QInputDialog.getItem(self, "Select a column",
                                                  "Select a column to remove", self.col_names[4:], 0, False)
        if accepted:
            self.subject_manager.delete_column(col_name)
            column = self.col_names.index(col_name)
            self.col_names.remove(col_name)
            self.tableWidget.removeColumn(column)

    def update_string(self, row, col):
        subject = self.subject_names[row]
        new_value = self.tableWidget.item(row, col).text()
        if col == 0:  # subject name
            if new_value in self.subject_names:
                self.show_warning("The name of this subject already exists")
                self.tableWidget.blockSignals(True)
                self.tableWidget.item(row, col).setText(self.subject_names[row])
                self.tableWidget.blockSignals(False)
                return
            self.subject_manager.update_subject(self.subject_names[row], new_value)
            self.subject_names[row] = subject

        elif col == 1:  # sensor ID
            self.subject_manager.update_sensor(self.subject_names[row], new_value)

        else:  # user-made column
            col_name = self.tableWidget.horizontalHeaderItem(col).text()
            self.subject_manager.update_user_column(col_name, subject, new_value)

    def update_date(self, date: QDate):
        row = self.tableWidget.currentRow()
        col = self.tableWidget.currentColumn()
        subject = self.subject_names[row]
        new_date = datetime(date.year(), date.month(), date.day())
        if col == 2:  # start date
            self.subject_manager.update_start_date(subject, new_date)
        else:  # end date
            self.subject_manager.update_end_date(subject, new_date)

    def show_warning(self, message: str):
        QMessageBox.warning(self, 'Warning', message, QMessageBox.Cancel)
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer_subject_table.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Subject_table(object):
    def setupUi(self, Subject_table):
        Subject_table.setObjectName("Subject_table")
        Subject_table.resize(537, 408)
        self.buttonBox = QtWidgets.QDialogButtonBox(Subject_table)
        self.buttonBox.setGeometry(QtCore.QRect(330, 370, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tableWidget = QtWidgets.QTableWidget(Subject_table)
        self.tableWidget.setGeometry(QtCore.QRect(5, 10, 521, 351))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.verticalHeader().setVisible(False)
        self.rowButton = QtWidgets.QPushButton(Subject_table)
        self.rowButton.setGeometry(QtCore.QRect(20, 370, 93, 28))
        self.rowButton.setObjectName("rowButton")
        self.colButton = QtWidgets.QPushButton(Subject_table)
        self.colButton.setGeometry(QtCore.QRect(130, 370, 93, 28))
        self.colButton.setObjectName("colButton")
        self.print = QtWidgets.QPushButton(Subject_table)
        self.print.setGeometry(QtCore.QRect(230, 370, 93, 28))
        self.print.setObjectName("print")

        self.retranslateUi(Subject_table)
        self.buttonBox.accepted.connect(Subject_table.accept)
        self.buttonBox.rejected.connect(Subject_table.reject)
        QtCore.QMetaObject.connectSlotsByName(Subject_table)

    def retranslateUi(self, Subject_table):
        _translate = QtCore.QCoreApplication.translate
        Subject_table.setWindowTitle(_translate("Subject_table", "Subject table"))
        self.rowButton.setText(_translate("Subject_table", "Add subject"))
        self.colButton.setText(_translate("Subject_table", "Add column"))
        self.print.setText(_translate("Subject_table", "print"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'labelspecs.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LabelSpecs(object):
    def setupUi(self, LabelSpecs):
        LabelSpecs.setObjectName("LabelSpecs")
        LabelSpecs.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(LabelSpecs)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(LabelSpecs)
        self.buttonBox.accepted.connect(LabelSpecs.accept)
        self.buttonBox.rejected.connect(LabelSpecs.reject)
        QtCore.QMetaObject.connectSlotsByName(LabelSpecs)

    def retranslateUi(self, LabelSpecs):
        _translate = QtCore.QCoreApplication.translate
        LabelSpecs.setWindowTitle(_translate("LabelSpecs", "Dialog"))


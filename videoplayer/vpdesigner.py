# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vpdesigner.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_videoplayer(object):
    def setupUi(self, videoplayer):
        videoplayer.setObjectName("videoplayer")
        videoplayer.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(videoplayer)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QVideoWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(30, 70, 421, 281))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(220, 30, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        videoplayer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(videoplayer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        videoplayer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(videoplayer)
        self.statusbar.setObjectName("statusbar")
        videoplayer.setStatusBar(self.statusbar)

        self.retranslateUi(videoplayer)
        QtCore.QMetaObject.connectSlotsByName(videoplayer)

    def retranslateUi(self, videoplayer):
        _translate = QtCore.QCoreApplication.translate
        videoplayer.setWindowTitle(_translate("videoplayer", "MainWindow"))
        self.label.setText(_translate("videoplayer", "Video"))

from PyQt5.QtMultimediaWidgets import QVideoWidget

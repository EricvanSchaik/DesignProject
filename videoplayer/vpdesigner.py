# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vpdesigner.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VideoPlayer(object):
    def setupUi(self, VideoPlayer):
        VideoPlayer.setObjectName("VideoPlayer")
        VideoPlayer.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(VideoPlayer)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QVideoWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(30, 70, 421, 281))
        self.widget.setObjectName("widget")
        self.widget_2 = QMediaPlayer(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(220, 30, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 360, 31, 31))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/pause-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 360, 31, 31))
        self.pushButton_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resources/1600.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton.raise_()
        self.widget.raise_()
        self.label.raise_()
        self.pushButton_2.raise_()
        VideoPlayer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(VideoPlayer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        VideoPlayer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(VideoPlayer)
        self.statusbar.setObjectName("statusbar")
        VideoPlayer.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(VideoPlayer)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("resources/Open-Folder-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon2)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtWidgets.QAction(VideoPlayer)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("resources/exit-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon3)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(VideoPlayer)
        self.pushButton.clicked.connect(self.widget_2.pause)
        self.pushButton.clicked.connect(self.pushButton.hide)
        self.pushButton.clicked.connect(self.pushButton_2.show)
        self.pushButton_2.clicked.connect(self.pushButton_2.hide)
        self.pushButton_2.clicked.connect(self.pushButton.show)
        self.pushButton_2.clicked.connect(self.widget_2.play)
        self.actionExit.triggered.connect(VideoPlayer.close)
        QtCore.QMetaObject.connectSlotsByName(VideoPlayer)

    def retranslateUi(self, VideoPlayer):
        _translate = QtCore.QCoreApplication.translate
        VideoPlayer.setWindowTitle(_translate("VideoPlayer", "VideoPlayer"))
        self.label.setText(_translate("VideoPlayer", "Video"))
        self.menuFile.setTitle(_translate("VideoPlayer", "File"))
        self.actionOpen.setText(_translate("VideoPlayer", "Open"))
        self.actionOpen.setToolTip(_translate("VideoPlayer", "Open clip"))
        self.actionOpen.setShortcut(_translate("VideoPlayer", "Ctrl+Q"))
        self.actionExit.setText(_translate("VideoPlayer", "Exit"))
        self.actionExit.setToolTip(_translate("VideoPlayer", "Exit application"))
        self.actionExit.setShortcut(_translate("VideoPlayer", "Ctrl+Q"))

from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

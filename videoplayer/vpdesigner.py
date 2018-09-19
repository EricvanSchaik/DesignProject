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
        self.widget.setGeometry(QtCore.QRect(30, 40, 421, 281))
        self.widget.setObjectName("widget")
        self.mediaplayer = QMediaPlayer(self.widget)
        self.mediaplayer.setObjectName("mediaplayer")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 0, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 330, 421, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setEnabled(False)
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/pause-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalSlider = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout.addWidget(self.horizontalSlider)
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
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resources/Open-Folder-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtWidgets.QAction(VideoPlayer)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("resources/exit-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon2)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(VideoPlayer)
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

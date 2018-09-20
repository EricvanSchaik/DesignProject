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
        VideoPlayer.resize(859, 703)
        self.centralwidget = QtWidgets.QWidget(VideoPlayer)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QVideoWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(30, 40, 421, 281))
        self.widget.setObjectName("widget")
        self.label_video = QtWidgets.QLabel(self.centralwidget)
        self.label_video.setGeometry(QtCore.QRect(210, 0, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_video.setFont(font)
        self.label_video.setObjectName("label_video")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 330, 421, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.playButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.playButton.setEnabled(False)
        self.playButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/pause-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playButton.setIcon(icon)
        self.playButton.setCheckable(False)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout.addWidget(self.playButton)
        self.horizontalSlider = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.label_duration = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_duration.setObjectName("label_duration")
        self.horizontalLayout.addWidget(self.label_duration)
        self.label_sensordata = QtWidgets.QLabel(self.centralwidget)
        self.label_sensordata.setGeometry(QtCore.QRect(170, 360, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_sensordata.setFont(font)
        self.label_sensordata.setObjectName("label_sensordata")
        self.mediaplayer = QMediaPlayer(self.centralwidget)
        self.mediaplayer.setObjectName("mediaplayer")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 390, 421, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_sensordata = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_sensordata.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_sensordata.setObjectName("verticalLayout_sensordata")
        VideoPlayer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(VideoPlayer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 859, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        VideoPlayer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(VideoPlayer)
        self.statusbar.setObjectName("statusbar")
        VideoPlayer.setStatusBar(self.statusbar)
        self.actionOpen_video = QtWidgets.QAction(VideoPlayer)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resources/file_light-15-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen_video.setIcon(icon1)
        self.actionOpen_video.setObjectName("actionOpen_video")
        self.actionExit = QtWidgets.QAction(VideoPlayer)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("resources/exit-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon2)
        self.actionExit.setObjectName("actionExit")
        self.actionOpen_sensordata = QtWidgets.QAction(VideoPlayer)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("resources/Open-Folder-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen_sensordata.setIcon(icon3)
        self.actionOpen_sensordata.setObjectName("actionOpen_sensordata")
        self.menuFile.addAction(self.actionOpen_video)
        self.menuFile.addAction(self.actionOpen_sensordata)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(VideoPlayer)
        self.actionExit.triggered.connect(VideoPlayer.close)
        QtCore.QMetaObject.connectSlotsByName(VideoPlayer)

    def retranslateUi(self, VideoPlayer):
        _translate = QtCore.QCoreApplication.translate
        VideoPlayer.setWindowTitle(_translate("VideoPlayer", "VideoPlayer"))
        self.label_video.setText(_translate("VideoPlayer", "Video"))
        self.label_duration.setText(_translate("VideoPlayer", "00:00:00"))
        self.label_sensordata.setText(_translate("VideoPlayer", "Sensordata"))
        self.menuFile.setTitle(_translate("VideoPlayer", "File"))
        self.actionOpen_video.setText(_translate("VideoPlayer", "Open Video"))
        self.actionOpen_video.setToolTip(_translate("VideoPlayer", "Open clip"))
        self.actionExit.setText(_translate("VideoPlayer", "Exit"))
        self.actionExit.setToolTip(_translate("VideoPlayer", "Exit application"))
        self.actionOpen_sensordata.setText(_translate("VideoPlayer", "Open Sensordata"))

from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

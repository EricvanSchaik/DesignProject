# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer_gui.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VideoPlayer(object):
    def setupUi(self, VideoPlayer):
        VideoPlayer.setObjectName("VideoPlayer")
        VideoPlayer.resize(716, 713)
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
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(470, 40, 211, 621))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_ = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_.setObjectName("verticalLayout_")
        self.verticalLayout_info = QtWidgets.QVBoxLayout()
        self.verticalLayout_info.setContentsMargins(-1, 100, -1, 0)
        self.verticalLayout_info.setObjectName("verticalLayout_info")
        self.label_date = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_date.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_date.setFont(font)
        self.label_date.setText("")
        self.label_date.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_date.setObjectName("label_date")
        self.verticalLayout_info.addWidget(self.label_date)
        self.label_time = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_time.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_time.setFont(font)
        self.label_time.setText("")
        self.label_time.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_time.setObjectName("label_time")
        self.verticalLayout_info.addWidget(self.label_time)
        self.label_camera = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_camera.setMinimumSize(QtCore.QSize(0, 50))
        self.label_camera.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_camera.setFont(font)
        self.label_camera.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_camera.setObjectName("label_camera")
        self.verticalLayout_info.addWidget(self.label_camera)
        self.comboBox_camera = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.comboBox_camera.setObjectName("comboBox_camera")
        self.verticalLayout_info.addWidget(self.comboBox_camera)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.lineEdit_camera = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_camera.setObjectName("lineEdit_camera")
        self.horizontalLayout_3.addWidget(self.lineEdit_camera)
        self.pushButton_camera_ok = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_camera_ok.setMaximumSize(QtCore.QSize(35, 16777215))
        self.pushButton_camera_ok.setObjectName("pushButton_camera_ok")
        self.horizontalLayout_3.addWidget(self.pushButton_camera_ok)
        self.verticalLayout_info.addLayout(self.horizontalLayout_3)
        self.pushButton_camera_del = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_camera_del.setFont(font)
        self.pushButton_camera_del.setObjectName("pushButton_camera_del")
        self.verticalLayout_info.addWidget(self.pushButton_camera_del)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_offset = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_offset.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_offset.setFont(font)
        self.label_offset.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_offset.setObjectName("label_offset")
        self.horizontalLayout_2.addWidget(self.label_offset)
        self.doubleSpinBox_offset = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.doubleSpinBox_offset.setDecimals(3)
        self.doubleSpinBox_offset.setMinimum(-99.99)
        self.doubleSpinBox_offset.setObjectName("doubleSpinBox_offset")
        self.horizontalLayout_2.addWidget(self.doubleSpinBox_offset)
        self.verticalLayout_info.addLayout(self.horizontalLayout_2)
        self.verticalLayout_.addLayout(self.verticalLayout_info)
        self.verticalLayout_controls = QtWidgets.QVBoxLayout()
        self.verticalLayout_controls.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_controls.setObjectName("verticalLayout_controls")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_speed = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_speed.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_speed.setFont(font)
        self.label_speed.setAlignment(QtCore.Qt.AlignCenter)
        self.label_speed.setObjectName("label_speed")
        self.horizontalLayout_4.addWidget(self.label_speed)
        self.doubleSpinBox_speed = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.doubleSpinBox_speed.setDecimals(2)
        self.doubleSpinBox_speed.setMinimum(0.0)
        self.doubleSpinBox_speed.setProperty("value", 1.0)
        self.doubleSpinBox_speed.setObjectName("doubleSpinBox_speed")
        self.horizontalLayout_4.addWidget(self.doubleSpinBox_speed)
        self.verticalLayout_controls.addLayout(self.horizontalLayout_4)
        spacerItem = QtWidgets.QSpacerItem(20, 300, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_controls.addItem(spacerItem)
        self.label_current_formula = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.label_current_formula.setFont(font)
        self.label_current_formula.setText("")
        self.label_current_formula.setAlignment(QtCore.Qt.AlignCenter)
        self.label_current_formula.setObjectName("label_current_formula")
        self.verticalLayout_controls.addWidget(self.label_current_formula)
        self.comboBox_plot = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.comboBox_plot.setObjectName("comboBox_plot")
        self.verticalLayout_controls.addWidget(self.comboBox_plot)
        self.label_formula_name = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_formula_name.setObjectName("label_formula_name")
        self.verticalLayout_controls.addWidget(self.label_formula_name)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_controls.addWidget(self.lineEdit_2)
        self.label_formula = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_formula.setObjectName("label_formula")
        self.verticalLayout_controls.addWidget(self.label_formula)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_controls.addWidget(self.lineEdit)
        self.pushButton_label = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_label.setObjectName("pushButton_label")
        self.verticalLayout_controls.addWidget(self.pushButton_label)
        self.verticalLayout_.addLayout(self.verticalLayout_controls)
        VideoPlayer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(VideoPlayer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 716, 21))
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
        self.actionSettings = QtWidgets.QAction(VideoPlayer)
        self.actionSettings.setObjectName("actionSettings")
        self.actionLabel_Settings = QtWidgets.QAction(VideoPlayer)
        self.actionLabel_Settings.setObjectName("actionLabel_Settings")
        self.actionSubject_Mapping = QtWidgets.QAction(VideoPlayer)
        self.actionSubject_Mapping.setObjectName("actionSubject_Mapping")
        self.menuFile.addAction(self.actionOpen_video)
        self.menuFile.addAction(self.actionOpen_sensordata)
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionLabel_Settings)
        self.menuFile.addAction(self.actionSubject_Mapping)
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
        self.label_camera.setText(_translate("VideoPlayer", "Camera ID"))
        self.label.setText(_translate("VideoPlayer", "Or: "))
        self.pushButton_camera_ok.setText(_translate("VideoPlayer", "Ok"))
        self.pushButton_camera_del.setText(_translate("VideoPlayer", "Delete camera"))
        self.label_offset.setText(_translate("VideoPlayer", "Video offset (s):"))
        self.label_speed.setText(_translate("VideoPlayer", "Speed:"))
        self.label_formula_name.setText(_translate("VideoPlayer", "Name"))
        self.label_formula.setText(_translate("VideoPlayer", "Regular Expression"))
        self.pushButton_label.setText(_translate("VideoPlayer", "Label"))
        self.menuFile.setTitle(_translate("VideoPlayer", "File"))
        self.actionOpen_video.setText(_translate("VideoPlayer", "Open Video"))
        self.actionOpen_video.setToolTip(_translate("VideoPlayer", "Open clip"))
        self.actionExit.setText(_translate("VideoPlayer", "Exit"))
        self.actionExit.setToolTip(_translate("VideoPlayer", "Exit application"))
        self.actionOpen_sensordata.setText(_translate("VideoPlayer", "Open Sensordata"))
        self.actionSettings.setText(_translate("VideoPlayer", "Import Settings"))
        self.actionLabel_Settings.setText(_translate("VideoPlayer", "Label Settings"))
        self.actionSubject_Mapping.setText(_translate("VideoPlayer", "Subject Mapping"))

from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

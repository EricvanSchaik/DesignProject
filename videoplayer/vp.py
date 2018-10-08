import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLayout

from datastorage import settings
from videoplayer.newproject import Ui_NewProject
from videoplayer.vpdesigner import Ui_VideoPlayer
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
import matplotlib.pyplot
from data_import import import_data
import video_metadata as vm
from datetime import timedelta
import matplotlib.animation
from datastorage.labelstorage import LabelManager
from PyQt5 import QtCore
from videoplayer.labelspecs import Ui_LabelSpecs
import os


def add_time_strings(time1, time2):
    return timedelta(hours=int(time1[0] + time1[1]), minutes=int(time1[3] + time1[4]), seconds=int(time1[6] + time1[
        7])) + timedelta(hours=int(time2[0] + time2[1]), minutes=int(time2[3] + time2[4]), seconds=int(time2[6] +
                                                                                                       time2[7]))


class VideoPlayer(QMainWindow, Ui_VideoPlayer):

    def __init__(self):
        super().__init__()
        # Initialize the generated UI from vpdesigner.py.
        self.setupUi(self)

        # Connect all the buttons to their appropriate helper functions.
        self.playButton.clicked.connect(self.play)
        self.actionOpen_video.triggered.connect(self.open_video)
        self.actionOpen_sensordata.triggered.connect(self.open_sensordata)

        # Connect the QMediaPlayer to the right widget.
        self.mediaplayer.setVideoOutput(self.widget)

        # Connect some events that QMediaPlayer generates to their appropriate helper functions.
        self.mediaplayer.positionChanged.connect(self.position_changed)
        self.mediaplayer.durationChanged.connect(self.duration_changed)

        # Connect the usage of the slider to its appropriate helper function.
        self.horizontalSlider.sliderMoved.connect(self.set_position)

        # Initialize the libraries that are needed to plot the sensor data, and add them to the GUI.
        self.figure = matplotlib.pyplot.figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.verticalLayout_sensordata.addWidget(self.canvas)

        self.seconds = 0
        self.minutes = 0
        self.hours = 0

        self.i = 0
        self.timer = QtCore.QTimer(self)
        self.prev_position = self.mediaplayer.position()

        self.pushButton_label.clicked.connect(self.open_dialog)

        self.project_dialog = NewProject()
        self.project_dialog.exec_()

        self.actionSettings.triggered.connect(self.open_settings)
        self.settings = self.project_dialog.new_settings

    def open_video(self):
        """
        A helper function that allows a user to open a video in the QMediaPlayer via the menu bar.
        :return:
        """
        self.video_filename, _ = QFileDialog.getOpenFileName(self, "Open Video", QDir.homePath())
        if self.video_filename != '':
            self.mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_filename)))
            self.mediaplayer.play()
            self.playButton.setEnabled(True)
            self.label_date.setText(vm.datetime_with_tz_to_string(vm.parse_start_time_from_file(self.video_filename),
                                                                  '%d-%B-%Y'))
            self.label_time.setText(vm.datetime_with_tz_to_string(vm.parse_start_time_from_file(self.video_filename),
                                                                  '%H:%M:%S'))

    def open_sensordata(self):
        """
        A helper function that allows a user to open a CSV file in the plotting canvas via the menu bar.
        :return:
        """
        filename, _ = QFileDialog.getOpenFileName(self, "Open Sensor Data", QDir.homePath())
        if filename != '':
            self.data = import_data.parse_csv(filename)
            self.figure.clear()
            self.dataplot = self.figure.add_subplot(111)
            data1 = self.data.where(self.data['Time'] < 30).dropna(subset=['Time'])
            data2 = self.data.drop(['Mx', 'My', 'Mz', 'T', 'Ay', 'Az', 'Gx', 'Gy', 'Gz'], axis=1)
            self.dataplot.plot(data2['Time'], data2['Ax'], ',-', linewidth=1.0)
            self.dataplot.axis([-10, 10, self.data['Ax'].min(), self.data['Ax'].max()])
            self.timer.timeout.connect(self.update_plot)
            self.timer.start(1)
            self.canvas.draw()

    def play(self):
        """
        A helper function that makes sure the play button pauses or plays the video, and switches the pause/play icons.
        :return:
        """
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            icon = QtGui.QIcon()
            self.mediaplayer.pause()
            icon.addPixmap(QtGui.QPixmap("resources/1600.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.playButton.setIcon(icon)
        else:
            icon = QtGui.QIcon()
            self.mediaplayer.play()
            icon.addPixmap(QtGui.QPixmap("resources/pause-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.playButton.setIcon(icon)

    def position_changed(self, position):
        """
        Every time QMediaPlayer generates the event that indicates that the video output has changed (which is
        continually if you play a video), this function updates the slider.
        :param position: The position of the video.
        :return:
        """
        self.horizontalSlider.setValue(position)
        self.label_duration.setText(self.ms_to_time(position))
        self.label_time.setText(str(add_time_strings(self.ms_to_time(position), vm.datetime_with_tz_to_string(
            vm.parse_start_time_from_file(self.video_filename), '%H:%M:%S'))))

    def update_plot(self):
        self.dataplot.axis([-10 + (self.mediaplayer.position() / 1000),
                            10 + (self.mediaplayer.position() / 1000), self.data['Ax'].min(),
                            self.data['Ax'].max()])
        self.canvas.draw()
        self.i += 0.01

    def set_position(self, position):
        """
        Every time the user uses the slider, this function updates the QMediaPlayer position.
        :param position: The position as indicated by the slider.
        :return:
        """
        self.mediaplayer.setPosition(position)

    def duration_changed(self, duration):
        """
        Every time the duration of the video in QMediaPlayer changes (which should be every time you open a new
        video), this function updates the range of the slider.
        :param duration: The duration of the (new) video.
        :return:
        """
        self.horizontalSlider.setRange(0, duration)

    def ms_to_time(self, duration):
        """
        A helper function that translates a certain amount of milliseconds to a readable HH:MM:SS string.
        :param duration: The number of milliseconds that corresponds to the position of the video.
        :return: A readable string that corresponds to duration in the format HH:MM:SS.
        """
        self.seconds = (duration // 1000) % 60
        seconds_str = "0" + str(self.seconds) if self.seconds < 10 else str(self.seconds)
        self.minutes = (duration // (1000 * 60)) % 60
        minutes_str = "0" + str(self.minutes) if self.minutes < 10 else str(self.minutes)
        self.hours = duration // (1000 * 60 * 60)
        hours_str = "0" + str(self.hours) if self.hours < 10 else str(self.hours)

        return hours_str + ":" + minutes_str + ":" + seconds_str

    def open_dialog(self):
        dialog = LabelSpecs(self.project_dialog.project_name)
        dialog.exec_()
        dialog.show()

    def open_settings(self):
        settings = SettingsDialog(self.settings)
        settings.exec_()
        settings.show()


class LabelSpecs(QtWidgets.QDialog, Ui_LabelSpecs):

    def __init__(self, project_name):
        super().__init__()
        # Initialize the generated UI from vpdesigner.py.
        self.setupUi(self)
        self.label = Label()
        self.doubleSpinBox_start.valueChanged.connect(self.start_changed)
        self.doubleSpinBox_end.valueChanged.connect(self.stop_changed)
        self.label_storage = LabelManager(project_name)
        self.accepted.connect(self.send_label)
        self.comboBox_labels.activated.connect(self.label_changed)

    def start_changed(self, value: float):
        self.label.start = value

    def stop_changed(self, value: float):
        self.label.stop = value

    def label_changed(self, label: str):
        self.label.label = label

    def send_label(self):
        self.label_storage.add_label(self.label.start, self.label.end, self.label.label, "")


class Label:

    def __init__(self):
        self.label = 0
        self.start = 0.00
        self.end = 0.00

    def setLabel(self, name: str):
        self.label = name

    def setStart(self, start: float):
        self.start = start

    def setEnd(self, end: float):
        self.end = end


def exit_project():
    sys.exit(0)


class NewProject(QtWidgets.QDialog, Ui_NewProject):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.accepted.connect(self.open_project)
        self.rejected.connect(exit_project)
        for folder in os.listdir("projects"):
            self.comboBox_existing.addItem(folder)
        self.lineEdit_new.textChanged.connect(self.text_changed)
        self.project_name = ""
        if os.listdir("projects"):
            self.project_name = os.listdir("projects")[0]
            self.spinBox_timerow.setEnabled(False)
            self.spinBox_timecol.setEnabled(False)
            self.spinBox_daterow.setEnabled(False)
            self.spinBox_datecol.setEnabled(False)
            self.spinBox_srrow.setEnabled(False)
            self.spinBox_srcol.setEnabled(False)
            self.spinBox_snrow.setEnabled(False)
            self.spinBox_sncol.setEnabled(False)
            self.spinBox_namesrow.setEnabled(False)
            self.lineEdit_comment.setEnabled(False)
        self.time_row = 3
        self.spinBox_timerow.valueChanged.connect(self.set_timerow)
        self.time_col = 3
        self.spinBox_timecol.valueChanged.connect(self.set_timecol)
        self.date_row = 3
        self.spinBox_daterow.valueChanged.connect(self.set_daterow)
        self.date_col = 2
        self.spinBox_datecol.valueChanged.connect(self.set_datecol)
        self.sr_row = 5
        self.spinBox_srrow.valueChanged.connect(self.set_srrow)
        self.sr_col = 2
        self.spinBox_srcol.valueChanged.connect(self.set_srcol)
        self.sn_row = 2
        self.spinBox_snrow.valueChanged.connect(self.set_snrow)
        self.sn_col = 5
        self.spinBox_sncol.valueChanged.connect(self.set_sncol)
        self.names_row = 8
        self.spinBox_namesrow.valueChanged.connect(self.set_namesrow)
        self.comment = ";"
        self.lineEdit_comment.textChanged.connect(self.set_comment)

    def open_project(self):
        if self.lineEdit_new.text():
            settings.new_project(self.project_name)
            self.new_settings = settings.Settings(self.project_name)
            self.new_settings.set_setting("time_row", self.time_row)
            self.new_settings.set_setting("time_col", self.time_col)
            self.new_settings.set_setting("date_row", self.date_row)
            self.new_settings.set_setting("date_col", self.date_col)
            self.new_settings.set_setting("sr_row", self.sr_row)
            self.new_settings.set_setting("sr_col", self.sr_col)
            self.new_settings.set_setting("sn_row", self.sn_row)
            self.new_settings.set_setting("sn_col", self.sn_col)
            self.new_settings.set_setting("names_row", self.names_row)
            self.new_settings.set_setting("comment", self.comment)
        self.new_settings = settings.Settings(self.project_name)

    def text_changed(self, new):
        if self.lineEdit_new.text():
            self.project_name = new

            self.comboBox_existing.setEnabled(False)
            self.spinBox_timerow.setEnabled(True)
            self.spinBox_timecol.setEnabled(True)
            self.spinBox_daterow.setEnabled(True)
            self.spinBox_datecol.setEnabled(True)
            self.spinBox_srrow.setEnabled(True)
            self.spinBox_srcol.setEnabled(True)
            self.spinBox_snrow.setEnabled(True)
            self.spinBox_sncol.setEnabled(True)
            self.spinBox_namesrow.setEnabled(True)
            self.lineEdit_comment.setEnabled(True)

            self.spinBox_timerow.setValue(3)
            self.spinBox_timecol.setValue(3)
            self.spinBox_daterow.setValue(3)
            self.spinBox_datecol.setValue(2)
            self.spinBox_srrow.setValue(5)
            self.spinBox_srcol.setValue(2)
            self.spinBox_snrow.setValue(2)
            self.spinBox_sncol.setValue(5)
            self.spinBox_namesrow.setValue(8)
            self.lineEdit_comment.setText(";")
        else:
            self.comboBox_existing.setEnabled(True)
            self.spinBox_timerow.setEnabled(False)
            self.spinBox_timecol.setEnabled(False)
            self.spinBox_daterow.setEnabled(False)
            self.spinBox_datecol.setEnabled(False)
            self.spinBox_srrow.setEnabled(False)
            self.spinBox_srcol.setEnabled(False)
            self.spinBox_snrow.setEnabled(False)
            self.spinBox_sncol.setEnabled(False)
            self.spinBox_namesrow.setEnabled(False)
            self.lineEdit_comment.setEnabled(False)

    def set_timerow(self, new):
        self.time_row = new

    def set_timecol(self, new):
        self.time_col = new

    def set_daterow(self, new):
        self.date_row = new

    def set_datecol(self, new):
        self.date_col = new

    def set_srrow(self, new):
        self.sr_row = new

    def set_srcol(self, new):
        self.sr_col = new

    def set_snrow(self, new):
        self.sn_row = new

    def set_sncol(self, new):
        self.sn_col = new

    def set_namesrow(self, new):
        self.names_row = new

    def set_comment(self, new):
        self.comment = new


class SettingsDialog(NewProject):

    def __init__(self, settings: settings.Settings):
        super().__init__()
        self.settings = settings
        self.rejected.disconnect()
        self.comboBox_existing.setParent(None)
        self.comboBox_existing.deleteLater()
        self.lineEdit_new.setParent(None)
        self.lineEdit_new.deleteLater()
        self.label.setParent(None)
        self.label.deleteLater()
        self.label_2.setParent(None)
        self.label_2.deleteLater()
        self.verticalLayout_7.removeItem(self.verticalLayout)
        self.spinBox_timerow.setEnabled(True)
        self.spinBox_timecol.setEnabled(True)
        self.spinBox_daterow.setEnabled(True)
        self.spinBox_datecol.setEnabled(True)
        self.spinBox_srrow.setEnabled(True)
        self.spinBox_srcol.setEnabled(True)
        self.spinBox_snrow.setEnabled(True)
        self.spinBox_sncol.setEnabled(True)
        self.spinBox_namesrow.setEnabled(True)
        self.lineEdit_comment.setEnabled(True)

        self.spinBox_timerow.setValue(settings.get_setting("time_row"))
        self.spinBox_timecol.setValue(settings.get_setting("time_col"))
        self.spinBox_daterow.setValue(settings.get_setting("date_row"))
        self.spinBox_datecol.setValue(settings.get_setting("date_col"))
        self.spinBox_srrow.setValue(settings.get_setting("sr_row"))
        self.spinBox_srcol.setValue(settings.get_setting("sr_col"))
        self.spinBox_snrow.setValue(settings.get_setting("sn_row"))
        self.spinBox_sncol.setValue(settings.get_setting("sn_col"))
        self.spinBox_namesrow.setValue(settings.get_setting("names_row"))
        self.lineEdit_comment.setText(settings.get_setting("comment"))

    def open_project(self):
        self.settings.set_setting("time_row", self.time_row)
        self.settings.set_setting("time_col", self.time_col)
        self.settings.set_setting("date_row", self.date_row)
        self.settings.set_setting("date_col", self.date_col)
        self.settings.set_setting("sr_row", self.sr_row)
        self.settings.set_setting("sr_col", self.sr_col)
        self.settings.set_setting("sn_row", self.sn_row)
        self.settings.set_setting("sn_col", self.sn_col)
        self.settings.set_setting("names_row", self.names_row)
        self.settings.set_setting("comment", self.comment)

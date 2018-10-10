from datetime import timedelta

import matplotlib.animation
import matplotlib.pyplot
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg

import video_metadata as vm
from data_import import sensor_data
from datastorage.labelstorage import LabelManager
from gui.designer_gui import Ui_VideoPlayer
from gui.label_dialog import LabelSpecs
from gui.new_dialog import NewProject
from gui.settings_dialog import SettingsDialog


def add_time_strings(time1, time2):
    """
    Helper function that takes the strings of two times in the HH:MM:SS format, and returns a string with of the
    result of addition of the two times.
    :param time1: The string of the first time of the addition.
    :param time2: The string of the second time of the addition.
    :return: The result of the addition of the two times, again as a string in the HH:MM:SS format.
    """
    return timedelta(hours=int(time1[0] + time1[1]), minutes=int(time1[3] + time1[4]), seconds=int(time1[6] + time1[
        7])) + timedelta(hours=int(time2[0] + time2[1]), minutes=int(time2[3] + time2[4]), seconds=int(time2[6] +
                                                                                                       time2[7]))


class GUI(QMainWindow, Ui_VideoPlayer):

    def __init__(self):
        super().__init__()
        # Initialize the generated UI from designer_gui.py.
        self.setupUi(self)

        # Connect all the buttons to their appropriate helper functions.
        self.playButton.clicked.connect(self.play)
        self.actionOpen_video.triggered.connect(self.open_video)
        self.actionOpen_sensordata.triggered.connect(self.open_sensordata)
        self.pushButton_label.clicked.connect(self.open_label)
        self.actionSettings.triggered.connect(self.open_settings)

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

        # Initialize a timer that makes sure that the sensor data plays smoothly.
        self.timer = QtCore.QTimer(self)

        # Before showing the full GUI, a dialog window needs to be prompted where the user can choose between an
        # existing project and a new project, in which case the settings need to be specified.
        self.project_dialog = NewProject()
        self.project_dialog.exec_()

        # Save the settings from the new project dialog window.
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
            self.sensordata = sensor_data.SensorData(filename, self.settings.settings_dict)
            self.data = self.sensordata.data
            self.figure.clear()
            self.dataplot = self.figure.add_subplot(111)
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
        """
        Every millisecond the timer triggers this function, which should update the plot to the current time.
        :return:
        """
        self.dataplot.axis([-10 + (self.mediaplayer.position() / 1000),
                            10 + (self.mediaplayer.position() / 1000), self.data['Ax'].min(),
                            self.data['Ax'].max()])
        self.canvas.draw()

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
        seconds = (duration // 1000) % 60
        seconds_str = "0" + str(seconds) if seconds < 10 else str(seconds)
        minutes = (duration // (1000 * 60)) % 60
        minutes_str = "0" + str(minutes) if minutes < 10 else str(minutes)
        hours = duration // (1000 * 60 * 60)
        hours_str = "0" + str(hours) if hours < 10 else str(hours)

        return hours_str + ":" + minutes_str + ":" + seconds_str

    def open_label(self):
        """
        Helper function that opens the label dialog window.
        :return:
        """
        self.label_storage = LabelManager(self.project_dialog.project_name)
        dialog = LabelSpecs(self.project_dialog.project_name, self.sensordata.metadata['sn'])
        dialog.exec_()
        dialog.show()
        print(self.label_storage.get_all_labels(self.sensordata.metadata['sn']))

    def open_settings(self):
        """
        Helper function that opens the settings dialog window.
        :return:
        """
        settings = SettingsDialog(self.settings)
        settings.exec_()
        settings.show()

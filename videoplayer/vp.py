import sys

from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton
from videoplayer.vpdesigner import Ui_VideoPlayer
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
import matplotlib.pyplot
from data_import import import_data
import video_metadata as vm
import pytz





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
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.verticalLayout_sensordata.addWidget(self.toolbar)
        self.verticalLayout_sensordata.addWidget(self.canvas)

        self.seconds = 0
        self.minutes = 0
        self.hours = 0

    def open_video(self):
        """
        A helper function that allows a user to open a video in the QMediaPlayer via the menu bar.
        :return:
        """
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video", QDir.homePath())
        if filename != '':
            self.mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.mediaplayer.play()
            self.playButton.setEnabled(True)
            # print(vm.datetime_with_tz_to_string(vm.parse_start_time_from_file(filename), pytz.timezone(
            #     'Europe/Amsterdam')))
            # print(vm.parse_start_time_from_file(filename))

    def open_sensordata(self):
        """
        A helper function that allows a user to open a CSV file in the plotting canvas via the menu bar.
        :return:
        """
        filename, _ = QFileDialog.getOpenFileName(self, "Open Sensor Data", QDir.homePath())
        if filename != '':
            self.data = import_data.parse_csv(filename)
            self.figure.clear()
            dataplot = self.figure.add_subplot(111)
            dataplot.plot(self.data.where(self.data['Time'] < 15).dropna(subset=['Time']), '*-')
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
        self.figure.clear()
        dataplot = self.figure.add_subplot(111)
        data1 = self.data.where((0 + (position // 1000)) < self.data['Time'])
        data2 = data1.where(data1['Time'] < 15 + (position // 1000))
        data3 = data2.dropna(subset=['Time'])
        dataplot.plot(data3.drop(['Time', 'Mx', 'My', 'Mz', 'T', 'Ay', 'Az', 'Gx', 'Gy', 'Gz'], axis=1), '*-')
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
        self.seconds = (duration // 1000) % 60
        seconds_str = "0" + str(self.seconds) if self.seconds < 10 else str(self.seconds)
        self.minutes = (duration // (1000 * 60)) % 60
        minutes_str = "0" + str(self.minutes) if self.minutes < 10 else str(self.minutes)
        self.hours = duration // (1000 * 60 * 60)
        hours_str = "0" + str(self.hours) if self.hours < 10 else str(self.hours)

        return hours_str + ":" + minutes_str + ":" + seconds_str


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vp = VideoPlayer()
    vp.show()
    sys.exit(app.exec_())

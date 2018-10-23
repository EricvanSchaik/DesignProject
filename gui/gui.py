from datetime import timedelta
from datetime import datetime

import matplotlib.animation
import matplotlib.pyplot as plt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg

import video_metadata as vm
from data_import import sensor_data
from datastorage.labelstorage import LabelManager
from datastorage.camerainfo import CameraManager
from datastorage.deviceoffsets import OffsetManager
from gui.designer_gui import Ui_VideoPlayer
from gui.label_dialog import LabelSpecs
from gui.label_settings_dialog import LabelSettingsDialog
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
    return timedelta(hours=int(time1[0:2]), minutes=int(time1[3:5]), seconds=int(time1[6:8])) + timedelta(hours=int(
        time2[0:2]), minutes=int(time2[3:5]), seconds=int(time2[6:8]))


class GUI(QMainWindow, Ui_VideoPlayer):

    def __init__(self):
        super().__init__()
        # Initialize the generated UI from designer_gui.py.
        self.color_dict = dict()
        self.setupUi(self)

        # Connect all the buttons to their appropriate helper functions.
        self.playButton.clicked.connect(self.play)
        self.actionOpen_video.triggered.connect(self.open_video)
        self.actionOpen_sensordata.triggered.connect(self.open_sensordata)
        self.pushButton_label.clicked.connect(self.open_label)
        self.actionSettings.triggered.connect(self.open_settings)
        self.actionLabel_Settings.triggered.connect(self.open_label_settings)
        self.lineEdit_camera.returnPressed.connect(self.add_camera)
        self.doubleSpinBox_offset.valueChanged.connect(self.change_offset)
        self.pushButton_camera_ok.clicked.connect(self.add_camera)
        self.pushButton_camera_del.clicked.connect(self.delete_camera)

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
        self.canvas.mpl_connect('button_press_event', self.onclick)
        self.canvas.mpl_connect('button_release_event', self.onrelease)

        # Initialize a timer that makes sure that the sensor data plays smoothly.
        self.timer = QtCore.QTimer(self)

        # Before showing the full GUI, a dialog window needs to be prompted where the user can choose between an
        # existing project and a new project, in which case the settings need to be specified.
        self.project_dialog = NewProject()
        self.project_dialog.exec_()

        # Save the settings from the new project dialog window.
        self.settings = self.project_dialog.new_settings

        self.label_storage = LabelManager(self.project_dialog.project_name)

        self.combidt = datetime(year=1970, month=1, day=1)

        self.sensordata = None

        self.camera_manager = CameraManager()
        self.offset_manager = OffsetManager()
        for camera in self.camera_manager.get_all_cameras():
            self.comboBox_camera.addItem(camera)

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
            self.data = self.sensordata.get_data()
            self.combidt = self.sensordata.metadata['datetime']
            self.figure.clear()
            self.dataplot = self.figure.add_subplot(111)

            for label_type in self.label_storage.get_label_types():
                self.color_dict[label_type[0]] = label_type[1]
            labels = self.label_storage.get_all_labels(self.sensordata.metadata['sn'])
            if labels:
                for i in range(len(labels)):
                    label_start = (labels[i][0] - self.sensordata.metadata['datetime']).total_seconds()
                    label_end = (labels[i][1] - self.sensordata.metadata['datetime']).total_seconds()
                    subdata = self.data.where(label_start < self.data['Time'])
                    subdata = subdata.where(self.data['Time'] < label_end)
                    self.dataplot.plot(subdata['Time'], subdata['Ax'], ',-', linewidth=1, color=self.color_dict[
                        labels[i][2]])
                    if not i:
                        subdata = self.data.where(self.data['Time'] < label_start)
                        self.dataplot.plot(subdata['Time'], subdata['Ax'], ',-', linewidth=1, color='grey')
                    if i == (len(labels)-1):
                        subdata = self.data.where(self.data['Time'] > label_end)
                        self.dataplot.plot(subdata['Time'], subdata['Ax'], ',-', linewidth=1, color='grey')
                    else:
                        subdata = self.data.where(self.data['Time'] > label_end)
                        subdata = subdata.where(subdata['Time'] < (labels[i+1][0] - self.sensordata.metadata[
                            'datetime']).total_seconds())
                        self.dataplot.plot(subdata['Time'], subdata['Ax'], ',-', linewidth=1, color='grey')
            else:
                self.dataplot.plot(self.data['Time'], self.data['Ax'], ',-', linewidth=1, color='grey')
            self.vertical_line = self.dataplot.axvline(x=0)
            self.vertical_line.set_color('red')
            self.dataplot.axis([10, 10, self.data['Ax'].min(), self.data['Ax'].max()])
            self.timer.timeout.connect(self.update_plot)
            self.timer.start(1)
            self.canvas.draw()
            if self.comboBox_camera.currentText():
                self.doubleSpinBox_offset.setValue(self.offset_manager.get_offset(self.comboBox_camera.currentText(),
                                                                            self.sensordata.metadata['sn'],
                                                                            self.sensordata.metadata['date']))
            for label in self.label_storage.get_all_labels(self.sensordata.metadata['sn']):
                self.dataplot.text(((label[0] - self.sensordata.metadata['datetime']).total_seconds() + (
                    (label[1] - self.sensordata.metadata['datetime']).total_seconds())) / 2,
                                   (self.data['Ax'].max() * (3 / 4)), label[2], horizontalalignment='center')

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
        xmin = -10 + (self.mediaplayer.position() / 1000) - self.doubleSpinBox_offset.value()
        xmax = 10 + (self.mediaplayer.position() / 1000) - self.doubleSpinBox_offset.value()
        self.dataplot.axis([xmin, xmax, self.data['Ax'].min(), self.data['Ax'].max()])
        self.vertical_line.set_xdata((xmin + xmax) / 2)
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
        if not self.sensordata:
            QMessageBox.information(self, 'Warning', "You need to import sensordata first.", QMessageBox.Ok)
        else:
            dialog = LabelSpecs(self.project_dialog.project_name, self.sensordata.metadata['sn'], self.label_storage,
                                self.combidt.timestamp())
            dialog.exec_()
            dialog.show()
            if dialog.is_accepted:
                self.dataplot.text((((datetime.fromtimestamp(dialog.label.start) - self.sensordata.metadata['datetime']).total_seconds())
                                + ((datetime.fromtimestamp(dialog.label.end) - self.sensordata.metadata[
                        'datetime']).total_seconds())) / 2,
                               self.data['Ax'].max() * (3 / 4), dialog.label.label)

    def open_settings(self):
        """
        Helper function that opens the settings dialog window.
        :return:
        """
        settings = SettingsDialog(self.settings)
        settings.exec_()
        settings.show()

    def open_label_settings(self):
        label_settings = LabelSettingsDialog(self.label_storage)
        label_settings.exec_()
        label_settings.show()
        if label_settings.is_accepted:
            self.reset_graph()

    def add_camera(self):
        if self.lineEdit_camera.text() and self.lineEdit_camera.text() not in self.camera_manager.get_all_cameras():
            self.camera_manager.add_camera(self.lineEdit_camera.text())
            self.comboBox_camera.addItem(self.lineEdit_camera.text())
            self.comboBox_camera.setCurrentText(self.lineEdit_camera.text())
            self.lineEdit_camera.clear()

    def change_offset(self):
        if self.comboBox_camera.currentText():
            self.offset_manager.set_offset(self.comboBox_camera.currentText(), self.sensordata.metadata['sn'],
                                           self.doubleSpinBox_offset.value(), self.sensordata.metadata['date'])

    def delete_camera(self):
        if self.comboBox_camera.currentText():
            reply = QMessageBox.question(self, 'Message', "Are you sure you want to delete the current camera?",
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.camera_manager.delete_camera(self.comboBox_camera.currentText())
                self.comboBox_camera.clear()
                for camera in self.camera_manager.get_all_cameras():
                    self.comboBox_camera.addItem(camera)
                self.doubleSpinBox_offset.clear()
                if self.comboBox_camera.currentText() and self.sensordata:
                    self.doubleSpinBox_offset.setValue(
                        self.offset_manager.get_offset(self.comboBox_camera.currentText(),
                                                       self.sensordata.metadata['sn'],
                                                       self.sensordata.metadata['date']))
                else:
                    self.doubleSpinBox_offset.setValue(0)

    def onclick(self, event):
        if self.sensordata:
            self.new_label = LabelSpecs(self.project_dialog.project_name, self.sensordata.metadata['sn'],
                                        self.label_storage, self.combidt.timestamp())
            self.new_label.doubleSpinBox_start.setValue(event.xdata)

    def onrelease(self, event):
        if self.sensordata:
            self.new_label.doubleSpinBox_end.setValue(event.xdata)
            self.new_label.exec_()
            if self.new_label.is_accepted:
                self.reset_graph()

    def reset_graph(self):
        self.dataplot.clear()

        for label_type in self.label_storage.get_label_types():
            self.color_dict[label_type[0]] = label_type[1]
        labels = self.label_storage.get_all_labels(self.sensordata.metadata['sn'])
        for i in range(len(labels)):
            label_start = (labels[i][0] - self.sensordata.metadata['datetime']).total_seconds()
            label_end = (labels[i][1] - self.sensordata.metadata['datetime']).total_seconds()
            subdata = self.data.where(label_start < self.data['Time'])
            subdata = subdata.where(self.data['Time'] < label_end)
            self.dataplot.plot(subdata['Time'], subdata['Ax'], ',-', linewidth=1, color=self.color_dict[
                labels[i][2]])
            if not i:
                subdata = self.data.where(self.data['Time'] < label_start)
                self.dataplot.plot(subdata['Time'], subdata['Ax'], ',-', linewidth=1, color='grey')
            if i == (len(labels) - 1):
                subdata = self.data.where(self.data['Time'] > label_end)
                self.dataplot.plot(subdata['Time'], subdata['Ax'], ',-', linewidth=1, color='grey')
            else:
                subdata = self.data.where(self.data['Time'] > label_end)
                subdata = subdata.where(subdata['Time'] < (labels[i + 1][0] - self.sensordata.metadata[
                    'datetime']).total_seconds())
                self.dataplot.plot(subdata['Time'], subdata['Ax'], ',-', linewidth=1, color='grey')
        self.vertical_line = self.dataplot.axvline(x=0)
        self.vertical_line.set_color('red')
        for label in self.label_storage.get_all_labels(self.sensordata.metadata['sn']):
            self.dataplot.text(((label[0] - self.sensordata.metadata['datetime']).total_seconds() + (
                (label[1] - self.sensordata.metadata['datetime']).total_seconds())) / 2,
                               (self.data['Ax'].max() * (3 / 4)), label[2], horizontalalignment='center')

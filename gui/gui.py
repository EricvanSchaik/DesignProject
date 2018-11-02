import os.path
from datetime import datetime
from datetime import timedelta

import matplotlib.animation
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, QDir, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QShortcut
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from sklearn.naive_bayes import GaussianNB

import video_metadata as vm
from data_export import export_data, windowing as wd
from data_import import sensor_data
from data_import.label_data import LabelData
from datastorage.camerainfo import CameraManager
from datastorage.deviceoffsets import OffsetManager
from datastorage.labelstorage import LabelManager
from datastorage.subjectmapping import SubjectManager
from gui.designer_gui import Ui_VideoPlayer
from gui.export_dialog import ExportDialog
from gui.label_dialog import LabelSpecs
from gui.label_settings_dialog import LabelSettingsDialog
from gui.machine_learning_dialog import MachineLearningDialog
from gui.new_dialog import NewProject
from gui.settings_dialog import SettingsDialog
from gui.subject_dialog import SubjectTable
from machine_learning.classifier import Classifier, make_predictions


LABEL_COL = 'Label'
TIME_COL = 'Time'
TIMESTAMP_COL = 'Timestamp'


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
        self.setupUi(self)

        # Initialize the dictionary that is used to map a label type to a color.
        self.color_dict = dict()

        # Initialize the dictionary that is used to map the name of a new formula to the formula itself (as a string).
        self.formula_dict = dict()

        # Initialize the boolean that keeps track if the user is labeling with the right-mouse button.
        self.labeling = False

        # Initialize the datetime object that keeps track of the start of a sensor data file.
        self.combidt = datetime(year=1970, month=1, day=1)

        # Initialize the variable that keeps track of the current SensorData object.
        self.sensordata = None

        # Used for retrieving and storing labels
        self.sensor_id = None

        # create key shortcuts
        self.shortcut_plus_10s = QShortcut(QKeySequence(QKeySequence.MoveToNextChar), self)
        self.shortcut_minus_10s = QShortcut(QKeySequence(QKeySequence.MoveToPreviousChar), self)
        self.shortcut_pause = QShortcut(Qt.Key_Space, self)

        # Connect all the buttons, spin boxes, combo boxes and line edits to their appropriate helper functions.
        self.playButton.clicked.connect(self.play)
        self.shortcut_pause.activated.connect(self.play)
        self.shortcut_plus_10s.activated.connect(self.video_plus_10s)
        self.shortcut_minus_10s.activated.connect(self.video_minus_10s)
        self.actionOpen_video.triggered.connect(self.open_video)
        self.actionOpen_sensordata.triggered.connect(self.open_sensordata)
        self.pushButton_label.clicked.connect(self.open_label)
        self.actionSettings.triggered.connect(self.open_settings)
        self.actionLabel_Settings.triggered.connect(self.open_label_settings)
        self.comboBox_camera.currentTextChanged.connect(self.change_camera)
        self.lineEdit_camera.returnPressed.connect(self.add_camera)
        self.lineEdit.returnPressed.connect(self.new_plot)
        self.doubleSpinBox_offset.valueChanged.connect(self.change_offset)
        self.doubleSpinBox_speed.valueChanged.connect(self.change_speed)
        self.comboBox_plot.activated.connect(self.change_plot)
        self.pushButton_camera_ok.clicked.connect(self.add_camera)
        self.pushButton_camera_del.clicked.connect(self.delete_camera)
        self.actionSubject_Mapping.triggered.connect(self.open_subject_mapping)
        self.actionExport_Sensordata.triggered.connect(self.open_export)
        self.actionMachine_Learning.triggered.connect(self.open_machine_learning)

        # Connect the QMediaPlayer to the right widget.
        self.mediaplayer.setVideoOutput(self.widget)

        # Connect some events that QMediaPlayer generates to their appropriate helper functions.
        self.mediaplayer.positionChanged.connect(self.position_changed)
        self.mediaplayer.durationChanged.connect(self.duration_changed)

        # Connect the usage of the slider to its appropriate helper function.
        self.horizontalSlider.sliderMoved.connect(self.set_position)
        self.horizontalSlider.setEnabled(False)

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

        # Initialize the classes that retrieve information from the database.
        self.camera_manager = CameraManager()
        self.offset_manager = OffsetManager()
        self.label_storage = LabelManager(self.project_dialog.project_name)
        self.label_data = LabelData(self.label_storage)
        self.subject_mapping = SubjectManager(self.project_dialog.project_name)

        # Add the known camera's to the camera combo box in the GUI.
        for camera in self.camera_manager.get_all_cameras():
            self.comboBox_camera.addItem(camera)

        # Machine learning fields
        self.ml_dataframe = None
        self.ml_classifier_engine = GaussianNB()
        self.ml_used_columns = []
        self.ml_classifier = Classifier(self.ml_classifier_engine)

    def open_video(self):
        """
        A function that allows a user to open a video in the QMediaPlayer via the menu bar.
        :return:
        """
        # Check if last used path is known.
        path = "" if self.settings.get_setting("last_videofile") is None else self.settings.get_setting("last_videofile")
        if not os.path.isfile(path):
            path = path.rsplit('/', 1)[0]
            if not os.path.isdir(path):
                path = QDir.homePath()

        # Get the user input from a dialog window.
        self.video_filename, _ = QFileDialog.getOpenFileName(self, "Open Video", path)

        # Save the path for next time.
        if self.video_filename != '':
            self.settings.set_setting("last_videofile", self.video_filename)

            # Play the video in the QMediaPlayer and activate the associated widgets.
            self.mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_filename)))
            self.mediaplayer.play()
            self.playButton.setEnabled(True)
            self.horizontalSlider.setEnabled(True)
            self.label_date.setText(vm.datetime_with_tz_to_string(vm.parse_start_time_from_file(self.video_filename),
                                                                  '%d-%B-%Y'))
            self.label_time.setText(vm.datetime_with_tz_to_string(vm.parse_start_time_from_file(self.video_filename),
                                                                  '%H:%M:%S'))

    def open_sensordata(self):
        """
        A function that allows a user to open a CSV file in the plotting canvas via the menu bar.
        :return:
        """
        # Check if last used path is known.
        path = "" if self.settings.get_setting("last_datafile") is None else self.settings.get_setting("last_datafile")
        if not os.path.isfile(path):
            path = path.rsplit('/', 1)[0]
            if not os.path.isdir(path):
                path = QDir.homePath()

        # Get the user input from a dialog window.
        filename, _ = QFileDialog.getOpenFileName(self, "Open Sensor Data", path)

        # Save the path for next time.
        if filename != '':
            self.settings.set_setting("last_datafile", filename)

            # Reset the dictionary that maps function names to functions.
            self.formula_dict = dict()

            # Retrieve the SensorData object that parses the sensor data file.
            self.sensordata = sensor_data.SensorData(filename, self.settings.settings_dict)
            self.sensor_id = self.sensordata.metadata['sn']

            # Retrieve the formulas that are associated with this sensor data file, and store them in the dictionary.
            stored_formulas = self.settings.get_setting("formulas")
            for formula_name in stored_formulas:
                try:
                    self.sensordata.add_column_from_func(formula_name, stored_formulas[formula_name])
                    self.formula_dict[formula_name] = stored_formulas[formula_name]
                except Exception as e:
                    print(e)

            # Retrieve the DataFrame with all the raw sensor data.
            self.data = self.sensordata.get_data()

            # Add every column in the DataFrame to the possible Data Series that can be plotted, except for time,
            # and plot the first one.
            for column in self.data.columns:
                self.comboBox_plot.addItem(column)
            self.comboBox_plot.removeItem(0)
            self.current_plot = self.comboBox_plot.currentText()

            self.combidt = self.sensordata.metadata['datetime']
            self.figure.clear()
            self.dataplot = self.figure.add_subplot(111)

            self.ymin = self.data[self.current_plot].min()
            self.ymax = self.data[self.current_plot].max()
            self.draw_graph()
            self.dataplot.axis([10, 10, self.ymin, self.ymax])
            self.timer.timeout.connect(self.update_plot)
            self.timer.start(1)
            self.canvas.draw()
            if self.comboBox_camera.currentText():
                self.doubleSpinBox_offset.setValue(self.offset_manager.get_offset(self.comboBox_camera.currentText(),
                                                                            self.sensordata.metadata['sn'],
                                                                            self.sensordata.metadata['date']))
            if not self.label_storage.file_is_added(filename):
                self.label_storage.add_file(filename, self.sensordata.metadata['sn'], self.combidt)

    def play(self):
        """
        A helper function that makes sure the play button pauses or plays the video, and switches the pause/play icons.
        :return:
        """
        if self.mediaplayer.media().isNull():
            return
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

    def video_plus_10s(self):
        if not self.mediaplayer.media().isNull():
            self.mediaplayer.setPosition(self.mediaplayer.position() + 10000)

    def video_minus_10s(self):
        if not self.mediaplayer.media().isNull():
            self.mediaplayer.setPosition(self.mediaplayer.position() - 10000)

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
        self.dataplot.axis([xmin, xmax, self.ymin, self.ymax])
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
                               self.ymax * (3 / 4), dialog.label.label)

    def open_settings(self):
        """
        Helper function that opens the settings dialog window.
        :return:
        """
        settings = SettingsDialog(self.settings)
        settings.exec_()
        settings.show()

    def open_label_settings(self):
        label_settings = LabelSettingsDialog(self.label_storage, self.settings)
        label_settings.exec_()
        label_settings.show()
        if label_settings.settings_changed:
            self.draw_graph()

    def open_subject_mapping(self):
        subject_mapping = SubjectTable(self.project_dialog.project_name)
        subject_mapping.exec_()
        subject_mapping.show()

    def open_export(self):
        export = ExportDialog()
        export.comboBox.addItems(self.subject_mapping.get_subjects())
        export.exec_()
        export.show()
        if export.is_accepted and export.comboBox.currentText():
            filename, _ = QFileDialog.getSaveFileName(self, "Save File", QDir.homePath())
            try:
                export_data.export(self.subject_mapping.get_dataframes_subject(export.comboBox.currentText()), "Label",
                                   "Timestamp", filename, [])
            except Exception as e:
                QMessageBox.warning(self, 'Warning', str(e), QMessageBox.Cancel)

    def open_machine_learning(self):

        columns = [self.comboBox_plot.itemText(i) for i in range(self.comboBox_plot.count())]
        dialog = MachineLearningDialog(columns)
        dialog.exec_()
        dialog.show()

        self.ml_used_columns = []
        funcs = {
            'mean': np.mean,
            'std': np.std
        }
        features = []

        if dialog.is_accepted and dialog.radioButton.isChecked():
            for column in columns:
                if dialog.column_dict[column]:
                    self.ml_used_columns.append(column)

                    for func in funcs:
                        features.append(column + '_' + func)

            if self.label_data.get_sensor_id() is None:
                if self.sensor_id is None:
                    raise Exception('self.sensor_id is None')

                self.label_data.set_sensor_id(self.sensor_id)

            self.ml_dataframe = self.sensordata.__copy__()
            self.ml_dataframe.add_timestamp_column(TIME_COL, TIMESTAMP_COL)
            self.ml_dataframe.add_labels(self.label_data.get_data(), LABEL_COL, TIMESTAMP_COL)
            raw_data = self.ml_dataframe.get_data()

            # Remove data points where label is unknown
            raw_data = raw_data[raw_data[LABEL_COL] != 'unknown']

            self.ml_dataframe = wd.windowing(raw_data, self.ml_used_columns, LABEL_COL, TIMESTAMP_COL, **funcs)
            self.ml_classifier.set_df(self.ml_dataframe)
            self.ml_classifier.set_features(features)
            res = self.ml_classifier.classify()

            for x in res:
                print(x)

            print(make_predictions(res))

    def add_camera(self):
        if self.lineEdit_camera.text() and self.lineEdit_camera.text() not in self.camera_manager.get_all_cameras():
            self.camera_manager.add_camera(self.lineEdit_camera.text())
            self.comboBox_camera.addItem(self.lineEdit_camera.text())
            self.comboBox_camera.setCurrentText(self.lineEdit_camera.text())
            self.lineEdit_camera.clear()
            if self.comboBox_camera.currentText() and self.sensordata:
                self.doubleSpinBox_offset.setValue(self.offset_manager.get_offset(self.comboBox_camera.currentText(),
                                                                            self.sensordata.metadata['sn'],
                                                                            self.sensordata.metadata['date']))

    def change_camera(self):
        if self.comboBox_camera.currentText() and self.sensordata:
            self.doubleSpinBox_offset.setValue(self.offset_manager.get_offset(self.comboBox_camera.currentText(),
                                                                              self.sensordata.metadata['sn'],
                                                                              self.sensordata.metadata['date']))

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

    def change_plot(self):
        self.current_plot = self.comboBox_plot.currentText()
        if self.comboBox_plot.currentText() in self.formula_dict:
            self.label_current_formula.setText(self.formula_dict[self.comboBox_plot.currentText()])
        self.ymin = self.data[self.current_plot].min()
        self.ymax = self.data[self.current_plot].max()
        self.draw_graph()

    def new_plot(self):
        try:
            if not self.lineEdit_2.text():
                raise Exception
            self.sensordata.add_column_from_func(self.lineEdit_2.text(), self.lineEdit.text())
            self.data = self.sensordata.get_data()
            self.comboBox_plot.addItem(self.lineEdit_2.text())
            self.formula_dict[self.lineEdit_2.text()] = self.lineEdit.text()
            stored_formulas = self.settings.get_setting("formulas")
            stored_formulas[self.lineEdit_2.text()] = self.lineEdit.text()
            self.settings.set_setting("formulas", stored_formulas)
            self.lineEdit.clear()
            self.lineEdit_2.clear()
        except:
            QMessageBox.warning(self, 'Warning', "Please enter a valid regular expression",
                                QMessageBox.Cancel)

    def change_speed(self):
        self.mediaplayer.setPlaybackRate(self.doubleSpinBox_speed.value())

    def onclick(self, event):
        if self.sensordata:
            if event.button == 1:
                self.new_label = LabelSpecs(self.project_dialog.project_name, self.sensordata.metadata['sn'],
                                            self.label_storage, self.combidt.timestamp())
                self.new_label.doubleSpinBox_start.setValue(event.xdata)
            elif event.button == 3:
                if not self.labeling:
                    self.large_label = LabelSpecs(self.project_dialog.project_name, self.sensordata.metadata['sn'],
                                                  self.label_storage, self.combidt.timestamp())
                    self.large_label.doubleSpinBox_start.setValue(event.xdata)
                else:
                    deleting = False
                    if event.xdata < self.large_label.doubleSpinBox_start.value():
                        self.large_label.doubleSpinBox_end.setValue(self.large_label.doubleSpinBox_start.value())
                        self.large_label.doubleSpinBox_start.setValue(event.xdata)
                    else:
                        self.large_label.doubleSpinBox_end.setValue(event.xdata)
                    start = self.large_label.doubleSpinBox_start.value()
                    end = self.large_label.doubleSpinBox_end.value()
                    for label in self.label_storage.get_labels_date(self.sensordata.metadata['sn'], self.sensordata.metadata['datetime'].date()):
                        label_start = (label[0] - self.sensordata.metadata['datetime']).total_seconds()
                        label_end = (label[1] - self.sensordata.metadata['datetime']).total_seconds()
                        if label_start < start < label_end and label_start < end < label_end:
                            deleting = True
                            delete_label = label
                            break
                        elif label_start < start < label_end or label_start < end < label_end:
                            if label_start < start < label_end:
                                self.large_label.doubleSpinBox_start.setValue(label_end)
                            else:
                                self.large_label.doubleSpinBox_end.setValue(label_start)
                    if deleting:
                        reply = QMessageBox.question(self, 'Message', "Are you sure you want to delete this label?",
                                                     QMessageBox.Yes, QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            self.label_storage.delete_label(delete_label[0], self.sensordata.metadata['sn'])
                            # remove label highlight and text from plot
                            self.label_highlights[(delete_label[0] - self.combidt).total_seconds()][0].remove()
                            self.label_highlights[(delete_label[0] - self.combidt).total_seconds()][1].remove()
                    else:
                        self.large_label.exec_()
                    if self.large_label.is_accepted:
                        new_label_start = (datetime.fromtimestamp(self.large_label.label.start) - self.combidt).total_seconds()
                        new_label_end = (datetime.fromtimestamp(self.large_label.label.end) - self.combidt).total_seconds()
                        self.add_label_highlight(new_label_start, new_label_end, self.large_label.label.label)
                        self.canvas.draw()
                self.labeling = not self.labeling

    def onrelease(self, event):
        if self.sensordata:
            if event.button == 1:
                deleting = False
                if event.xdata < self.new_label.doubleSpinBox_start.value():
                    self.new_label.doubleSpinBox_end.setValue(self.new_label.doubleSpinBox_start.value())
                    self.new_label.doubleSpinBox_start.setValue(event.xdata)
                else:
                    self.new_label.doubleSpinBox_end.setValue(event.xdata)
                start = self.new_label.doubleSpinBox_start.value()
                end = self.new_label.doubleSpinBox_end.value()
                for label in self.label_storage.get_labels_date(self.sensordata.metadata['sn'], self.sensordata.metadata['datetime'].date()):
                    label_start = (label[0] - self.sensordata.metadata['datetime']).total_seconds()
                    label_end = (label[1] - self.sensordata.metadata['datetime']).total_seconds()
                    if label_start < start < label_end and label_start < end < label_end:
                        deleting = True
                        delete_label = label
                        break
                    elif label_start < start < label_end or label_start < end < label_end:
                        if label_start < start < label_end:
                            self.new_label.doubleSpinBox_start.setValue(label_end)
                        else:
                            self.new_label.doubleSpinBox_end.setValue(label_start)
                if deleting:
                    reply = QMessageBox.question(self, 'Message', "Are you sure you want to delete this label?",
                                                 QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.label_storage.delete_label(delete_label[0], self.sensordata.metadata['sn'])
                        # remove label highlight and text from plot
                        self.label_highlights[(delete_label[0] - self.combidt).total_seconds()][0].remove()
                        self.label_highlights[(delete_label[0] - self.combidt).total_seconds()][1].remove()
                else:
                    self.new_label.exec_()
                if self.new_label.is_accepted:
                    new_label_start = (datetime.fromtimestamp(self.new_label.label.start) - self.combidt).total_seconds()
                    new_label_end = (datetime.fromtimestamp(self.new_label.label.end) - self.combidt).total_seconds()
                    self.add_label_highlight(new_label_start, new_label_end, self.new_label.label.label)
                    self.canvas.draw()
            elif event.button == 3:
                pass

    def draw_graph(self):
        if not self.sensordata:
            return
        self.dataplot.clear()

        self.dataplot.plot(self.data[self.data.columns[0]], self.data[self.current_plot], ',-', linewidth=1, color='black')
        self.vertical_line = self.dataplot.axvline(x=0)
        self.vertical_line.set_color('red')

        for label_type in self.label_storage.get_label_types():
            self.color_dict[label_type[0]] = label_type[1]
        labels = self.label_storage.get_labels_date(self.sensordata.metadata['sn'], self.sensordata.metadata['datetime'].date())
        self.label_highlights = {}
        for label in labels:
            label_start = (label[0] - self.sensordata.metadata['datetime']).total_seconds()
            label_end = (label[1] - self.sensordata.metadata['datetime']).total_seconds()
            self.add_label_highlight(label_start, label_end, label[2])
        self.canvas.draw()

    def add_label_highlight(self, label_start: float, label_end: float, label_type: str):
        alpha = self.settings.get_setting("label_opacity") / 100
        span = self.dataplot.axvspan(label_start, label_end, facecolor=self.color_dict[label_type], alpha=alpha)
        text = self.dataplot.text((label_start + label_end) / 2, self.ymax * 0.75, label_type, horizontalalignment='center')
        self.label_highlights[label_start] = (span, text)

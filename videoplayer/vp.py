import sys

from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from videoplayer.vpdesigner import Ui_VideoPlayer


def ms_to_time(duration):
    seconds = (duration//1000) % 60
    seconds = "0" + str(seconds) if seconds < 10 else str(seconds)
    minutes = (duration//(1000*60)) % 60
    minutes = "0" + str(minutes) if minutes < 10 else str(minutes)
    hours = duration//(1000*60*60)
    hours = "0" + str(hours) if hours < 10 else str(hours)

    return hours + ":" + minutes + ":" + seconds


class VideoPlayer(QMainWindow, Ui_VideoPlayer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.playButton.clicked.connect(self.play)
        self.actionOpen_video.triggered.connect(self.open_video)
        self.mediaplayer.setVideoOutput(self.widget)
        self.mediaplayer.positionChanged.connect(self.position_changed)
        self.horizontalSlider.sliderMoved.connect(self.set_position)
        self.mediaplayer.durationChanged.connect(self.duration_changed)

    def open_video(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
        if filename != '':
            self.mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.mediaplayer.play()
            self.playButton.setEnabled(True)

    def play(self):
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
        self.horizontalSlider.setValue(position)
        self.label_duration.setText(ms_to_time(position))

    def set_position(self, position):
        self.mediaplayer.setPosition(position)

    def duration_changed(self, duration):
        self.horizontalSlider.setRange(0, duration)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vp = VideoPlayer()
    vp.show()
    sys.exit(app.exec_())

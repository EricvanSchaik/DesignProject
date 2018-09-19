import sys

from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from videoplayer.vpdesigner import Ui_VideoPlayer


class VideoPlayer(QMainWindow, Ui_VideoPlayer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.play)
        self.actionOpen.triggered.connect(self.openfile)
        self.mediaplayer.setVideoOutput(self.widget)
        self.mediaplayer.positionChanged.connect(self.position_changed)
        self.horizontalSlider.sliderMoved.connect(self.set_position)
        self.mediaplayer.durationChanged.connect(self.duration_changed)

    def openfile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
        if filename != '':
            self.mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.mediaplayer.play()
            self.pushButton.setEnabled(True)

    def play(self):
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            icon = QtGui.QIcon()
            self.mediaplayer.pause()
            icon.addPixmap(QtGui.QPixmap("resources/1600.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton.setIcon(icon)
        else:
            icon = QtGui.QIcon()
            self.mediaplayer.play()
            icon.addPixmap(QtGui.QPixmap("resources/pause-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton.setIcon(icon)

    def position_changed(self, position):
        self.horizontalSlider.setValue(position)

    def set_position(self, position):
        self.mediaplayer.setPosition(position)

    def duration_changed(self, duration):
        self.horizontalSlider.setRange(0, duration)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vp = VideoPlayer()
    vp.show()
    sys.exit(app.exec_())

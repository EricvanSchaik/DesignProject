import sys
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSlider, \
    QStyle, QVBoxLayout, QWidget, QMainWindow, QAction
from PyQt5.QtGui import QIcon
from VideoPlayer import Ui_MainWindow


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.widget)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("D:\Google Drive\Series\Watchlist\Westworld\Westworld.Season.2.S02.1080p.AMZN.WEBRip.5.1.HEVC.x265-GIRAYS\Westworld.S02E08.Kiksuya.1080p.AMZN.WEB-DL.5.1.HEVC.x265-GIRAYS.v2\Westworld.S02E08.Kiksuya.1080p.AMZN.WEB-DL.5.1.HEVC.x265-GIRAYS.v2.mkv")))
        self.mediaPlayer.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

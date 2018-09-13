import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QMainWindow
from videoplayer.vpdesigner import Ui_videoplayer


class Example(QMainWindow, Ui_videoplayer):
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

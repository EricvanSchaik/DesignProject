import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QMainWindow
from videoplayer.vpdesigner import Ui_VideoPlayer


class Example(QMainWindow, Ui_VideoPlayer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.widget_2.setVideoOutput(self.widget)
        self.widget_2.setMedia(QMediaContent(QUrl.fromLocalFile("D:\Google Drive\Movies\Watchlist\A Quiet Place (2018) [WEBRip] [1080p] [YTS.AM]\A.Quiet.Place.2018.1080p.WEBRip.x264-[YTS.AM].mp4")))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

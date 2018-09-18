import sys
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from videoplayer.vpdesigner import Ui_VideoPlayer


class Example(QMainWindow, Ui_VideoPlayer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.openFile)
        self.widget_2.setVideoOutput(self.widget)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())

        if fileName != '':
            self.widget_2.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

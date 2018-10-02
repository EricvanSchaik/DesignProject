import sys

from PyQt5.QtWidgets import QApplication
from videoplayer import vp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    project = vp.VideoPlayer()
    project.show()
    sys.exit(app.exec_())

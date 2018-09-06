import sys
from PyQt5 import QtWidgets


def window():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    b = QtWidgets.QLabel(w)
    b.setText("Hello World!")
    w.setGeometry(100, 100, 200, 50)
    w.show()
    sys.exc_info(app.exec_())


if __name__ == '__main__':
    window()

import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication
from detemain import Mainwin


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)  
    w = Mainwin()
    w.resize(900, 750)
    w.show()
    sys.exit(app.exec_())
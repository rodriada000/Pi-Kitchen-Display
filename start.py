# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
from MainWindow import Ui_MainWindow

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()

    myapp = StartQT4()
    myapp.resize(width, height)
    myapp.showMaximized()
    sys.exit(app.exec_())

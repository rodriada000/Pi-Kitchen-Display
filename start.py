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
    QtGui.QFontDatabase.addApplicationFont("font/OSP-DIN.ttf")

    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()

    myapp = StartQT4()
    myapp.resize(width, height)

    # create gradient
    p = QtGui.QPalette()
    gradient = QtGui.QLinearGradient(0, 0, 0, height)
    gradient.setColorAt(1.0, QtGui.QColor(110, 152, 236))
    gradient.setColorAt(0.5, QtGui.QColor(191, 210, 250))
    gradient.setColorAt(0.0, QtGui.QColor(250, 250, 250))
    p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
    myapp.setPalette(p)
    
    myapp.showMaximized()
    sys.exit(app.exec_())

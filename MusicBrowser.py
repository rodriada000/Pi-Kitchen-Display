# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui, QtWebKit

class MusicPage(QtGui.QWidget):

    def __init__(self, parent, size):
        """
            Initialize the browser GUI and connect the events
        """
        super(MusicPage, self).__init__(parent)

        self.resize(size.width(), size.height())
        self.initUI(size)

    def initUI(self, size):

        self.grid = QtGui.QGridLayout(self)
        self.page = QtWebKit.QWebView()
        self.hideButton = QtGui.QPushButton()
        self.refreshBtn = QtGui.QPushButton()

        self.hideButton.setText("Minimize")
        self.hideButton.setMinimumHeight(25)
        self.hideButton.clicked.connect(self.hide)

        self.refreshBtn.setText("Refresh")
        self.refreshBtn.setMinimumHeight(25)
        self.refreshBtn.clicked.connect(self.reloadPlayer)

        try:
            self.page.load(QtCore.QUrl("http://192.168.1.7:4200"))
        except:
            self.page.load(QtCore.QUrl("http://www.google.com"))

        self.grid.addWidget(self.hideButton, 0, 0)
        self.grid.addWidget(self.refreshBtn, 0, 1)
        self.grid.addWidget(self.page, 1, 0, 2, 2)

        self.grid.setContentsMargins(0,0,0,0)
        self.grid.setSpacing(2)

        self.setLayout(self.grid)
        self.show()

    def reloadPlayer(self):
        self.page.load(QtCore.QUrl("http://192.168.1.7:4200"))

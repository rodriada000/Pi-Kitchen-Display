# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui, QtWebKit

class WebPage(QtGui.QWidget):

    def __init__(self, parent, size, url):
        """
            Initialize the browser GUI and connect the events
        """
        super(WebPage, self).__init__(parent)
        
        self.resize(size.width(), size.height())
        self.initUI(url)

    def initUI(self, url):
        
        self.vlay = QtGui.QVBoxLayout(self)
        self.hlay = QtGui.QHBoxLayout()
        
        self.page = QtWebKit.QWebView()
        if url is None:
            self.page.load(QtCore.QUrl("http://www.google.com")) # homepage is google
        else:
            self.page.load(QtCore.QUrl(url))
        
        self.pushBtn_close = QtGui.QPushButton()
        self.pushBtn_close.setText("X")
        
        self.lineEdit_url = QtGui.QLineEdit()
        
        self.pushBtn_go = QtGui.QPushButton()
        self.pushBtn_go.setText("->")
        
        self.pushBtn_refresh = QtGui.QPushButton()
        self.pushBtn_refresh.setText("↻")
        
        self.hlay.addWidget(self.pushBtn_close)
        self.hlay.addWidget(self.lineEdit_url)
        self.hlay.addWidget(self.pushBtn_go)
        self.hlay.addWidget(self.pushBtn_refresh)
        
        self.vlay.addLayout(self.hlay)
        self.vlay.addWidget(self.page)
        
        self.show()
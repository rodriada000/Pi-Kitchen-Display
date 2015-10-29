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
        self.hlay = QtGui.QHBoxLayout() # Layouts

        self.page = QtWebKit.QWebView()
        self.page.loadFinished.connect(self.onDone)
        if url is None:
            self.page.setUrl(QtCore.QUrl("http://www.google.com")) # homepage is google
        else:
            self.page.setUrl(QtCore.QUrl(url))
        self.page.load(self.page.url())
        self.page.urlChanged.connect(self.urlChanged)
        
        self.pushBtn_close = QtGui.QPushButton()
        self.pushBtn_close.setText("Exit")
        self.pushBtn_close.setMinimumWidth(15)
        self.pushBtn_close.clicked.connect(self.closeWeb) # Close button

        self.pushBtn_back = QtGui.QPushButton()
        self.pushBtn_back.setText("◀")
        self.pushBtn_back.setMinimumWidth(15)
        self.pushBtn_back.clicked.connect(self.page.back) # Back button

        self.pushBtn_forward = QtGui.QPushButton()
        self.pushBtn_forward.setText("▶")                 # Forward button
        self.pushBtn_forward.setMinimumWidth(15)
        self.pushBtn_forward.clicked.connect(self.page.forward)
        
        self.lineEdit_url = QtGui.QLineEdit()
        self.lineEdit_url.setText(self.page.url().toString()) # Address bar
        
        self.pushBtn_go = QtGui.QPushButton()
        self.pushBtn_go.setText("Go")
        self.pushBtn_go.clicked.connect(self.loadPage) 
        self.pushBtn_go.setShortcut("Return")               # Go button
        
        self.pushBtn_refresh = QtGui.QPushButton()
        self.pushBtn_refresh.setText("↻")
        self.pushBtn_refresh.clicked.connect(self.page.reload) # Refresh button
        
        self.hlay.addWidget(self.pushBtn_close)
        self.hlay.addWidget(self.pushBtn_back)
        self.hlay.addWidget(self.pushBtn_forward)
        self.hlay.addWidget(self.pushBtn_refresh)
        self.hlay.addWidget(self.lineEdit_url)
        self.hlay.addWidget(self.pushBtn_go)
        
        self.vlay.setContentsMargins(0,0,0,0)
        self.vlay.setSpacing(1)
        self.vlay.addLayout(self.hlay)
        self.vlay.addWidget(self.page)
        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) # have widget deleted on close
        self.show()
    #def end

    def closeWeb(self):
        self.close()
        return
    #def end

    def loadPage(self):
        url = self.lineEdit_url.text()
        http = "http://"
        www = "www."

        if (http not in url) and (www in url): # format is www.google.com
            url = http + url
        elif (http not in url) and (www not in url): # format is google.com
            url = http + www + url
        elif (http in url) and (www not in url): # format is http://google.com
            url = url

        self.lineEdit_url.setText(url)
        self.page.load(QtCore.QUrl(url))
        return
    #def end

    def urlChanged(self):
        self.lineEdit_url.setText(self.page.url().toString())
    #def end

    def onDone(self):
        print("page loaded...")
        return
    #def end
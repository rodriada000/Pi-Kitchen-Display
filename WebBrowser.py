# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
from PyQt4.QtNetwork import QNetworkAccessManager
from abpy import Filter

print("loading adblock filter ...")
adblockFilter = Filter(open("easylist.txt", 'r', encoding='utf-8'))
print("done.")

class MyNetworkAccessManager(QNetworkAccessManager): # inherited class that is modified to ignore network requests from known ad sources
    def createRequest(self, op, request, device=None):
        url = request.url().toString()
        doFilter = adblockFilter.match(url)
        if doFilter:
            try:
                return QNetworkAccessManager.createRequest(self, self.GetOperation, QtNetwork.QNetworkRequest(QtCore.QUrl()))
            except:
                print("failed to create request ...")
                
        return QNetworkAccessManager.createRequest(self, op, request, device)

class WebPage(QtGui.QWidget):

    def __init__(self, parent, size, url):
        """
            Initialize the browser GUI and connect the events
        """
        super(WebPage, self).__init__(parent)
        self.myNetAccessManager = MyNetworkAccessManager()
        
        self.resize(size.width(), size.height())
        self.initUI(size, url)

    def initUI(self, size, url):
        
        self.vlay = QtGui.QVBoxLayout(self)
        self.hlay = QtGui.QHBoxLayout() # Layouts
        
        self.pbar = QtGui.QProgressBar() # progress bar to go across bottom
        self.pbar.setStyleSheet("""QProgressBar { border: 2px solid grey; border-radius: 3px; background-color: #FF0000;}

 QProgressBar::chunk:horizontal {background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 cyan, stop: 1 white);}""")
        self.pbar.setMinimumWidth(size.width())
        self.pbar.setMaximumHeight(12)
        self.pbar.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.pbar.setTextVisible(False)
        self.pbar.move(0, size.height()-12)

        self.web = QtWebKit.QWebView(loadProgress = self.pbar.setValue, loadFinished = self.pbar.hide, loadStarted = self.pbar.show)
        self.web.page().setNetworkAccessManager(self.myNetAccessManager)
        
        if url is None:
            self.web.setUrl(QtCore.QUrl("http://www.google.com")) # homepage is google
        else:
            self.web.setUrl(QtCore.QUrl(url))
        
        self.web.urlChanged.connect(self.urlChanged)
        self.web.load(self.web.url())
        
        self.pushBtn_close = QtGui.QPushButton()
        self.pushBtn_close.setText("Exit")
        self.pushBtn_close.setMaximumWidth(35)
        self.pushBtn_close.clicked.connect(self.closeWeb) # Close button

        self.pushBtn_back = QtGui.QPushButton()
        self.pushBtn_back.setText("◀")
        self.pushBtn_back.setMaximumWidth(30)
        self.pushBtn_back.clicked.connect(self.web.back) # Back button

        self.pushBtn_forward = QtGui.QPushButton()
        self.pushBtn_forward.setText("▶")                 # Forward button
        self.pushBtn_forward.setMaximumWidth(30)
        self.pushBtn_forward.clicked.connect(self.web.forward)
        
        self.pushBtn_refresh = QtGui.QPushButton()
        self.pushBtn_refresh.setText("↻")
        self.pushBtn_refresh.clicked.connect(self.web.reload) # Refresh button
        self.pushBtn_refresh.setMaximumWidth(30)


        self.lineEdit_url = QtGui.QLineEdit()
        self.lineEdit_url.setText(self.web.url().toString()) # Address bar
        
        self.pushBtn_go = QtGui.QPushButton()
        self.pushBtn_go.setText("Go")
        self.pushBtn_go.setMaximumWidth(40)
        self.pushBtn_go.clicked.connect(self.loadPage)
        self.pushBtn_go.setShortcut("Return")               # Go button
        
        self.pushBtn_zoom = QtGui.QPushButton()
        self.pushBtn_zoom.setText("100%")
        self.pushBtn_zoom.setMaximumWidth(40)
        self.pushBtn_zoom.clicked.connect(self.changeZoom)

        self.hlay.addWidget(self.pushBtn_close)
        self.hlay.addWidget(self.pushBtn_back)
        self.hlay.addWidget(self.pushBtn_forward)
        self.hlay.addWidget(self.pushBtn_refresh)
        self.hlay.addWidget(self.lineEdit_url)
        self.hlay.addWidget(self.pushBtn_go)
        self.hlay.addWidget(self.pushBtn_zoom)
        
        self.vlay.setContentsMargins(0,0,0,0)
        self.vlay.setSpacing(1)
        self.vlay.addLayout(self.hlay)
        self.vlay.addWidget(self.web)
        
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
        com = ".com"

        if (http not in url) and (www not in url) and (com not in url): # perform a google search
            url = "http://www.google.com/search?q=" + url.replace(' ', '+')
        elif (http not in url) and (www in url): # format is www.google.com
            url = http + url
        elif (http not in url) and (www not in url): # format is google.com
            url = http + www + url
        elif (http in url) and (www not in url): # format is http://google.com
            url = url

        self.web.load(QtCore.QUrl(url))
        return
    #def end

    def urlChanged(self):
        self.lineEdit_url.setText(self.web.url().toString())
    #def end

    def changeZoom(self):
        zoom = self.web.zoomFactor()
        zoom -= 0.1;

        if zoom < 0.4:
            zoom = 1.0

        self.web.setZoomFactor(zoom)
        self.pushBtn_zoom.setText(str(round(zoom,1)*100)[:-2] + "%") # [:-2] changes 80.0% to 80%
    #def end
        

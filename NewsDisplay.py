# -*- coding: utf-8 -*-
import pyowm
import feedparser
from time import *
#from datetime import datetime
from PyQt4 import QtCore, QtGui
from WebBrowser import WebPage
from ExtendedQLabel import ClickableQLabel

class NewsWidget(QtGui.QWidget):

    articleClicked = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(NewsWidget, self).__init__(parent)
        
        self.rssList = list() # contatins all rss urls
        self.feedList = list() # contains all rss feed objects
        self.rssLinks = dict() # contains all links to displayed articles. key is article title, value is url
        
        try:
            with open('rssfeed.cfg') as urls:
                lines = [line.rstrip('\n') for line in urls]
                for rss in lines:
                    if rss[0] == '#': continue
                    self.rssList.append(rss)
        except:
            print("Failed to open rssfeed.cfg ...")
            return
        
        #Initialize timers
        self.updateTimer = QtCore.QTimer()
        self.updateTimer.timeout.connect(self.updateUI)
        self.updateTimer.start(3600000) # Update articles every hour
        
        self.initUI()
    #end def
        
    def initUI(self):
        self.vLay = QtGui.QVBoxLayout(self)
        self.vLay.setSpacing(0)
        
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidgetResizable(True)
        
        font = QtGui.QFont("Arial")
        font.setItalic(True)
        font.setPointSize(8)

        self.hbox = QtGui.QHBoxLayout(self)
        
        self.updateLbl = QtGui.QLabel()
        self.updateLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignBottom)
        self.updateLbl.setFont(font)

        self.upBtn = QtGui.QPushButton()
        self.upBtn.setText("Scroll Up")
        self.upBtn.clicked.connect(self.scrollUp)
        
        self.downBtn = QtGui.QPushButton()
        self.downBtn.setText("Scroll Down")
        self.downBtn.clicked.connect(self.scrollDown)
        
        self.hbox.addWidget(self.upBtn)
        self.hbox.addWidget(self.downBtn)
        self.hbox.addWidget(self.updateLbl)
        
        self.vLay.addLayout(self.hbox)
        self.vLay.addWidget(self.scroll)

        self.updateUI()
    #end def
        
    def updateUI(self):
        self.feedList = self.getFeeds() # get new feed objects
        w = self.updateArticles()
        self.updateLbl.setText(strftime("Updated at %-I:%M"))
        self.scroll.setWidget(w)
        
    def getFeeds(self):
        f = list()
        for url in self.rssList:
            f.append(feedparser.parse(url))
        return f
        
    def updateArticles(self):
        w = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(w)
        font = QtGui.QFont("Arial")
        i = 0
        
        self.rssLinks.clear() # remove all previous articles
        while i < 20:
            for feed in self.feedList:
                if i >= len(feed.entries): # verify that an entry exists
                    continue
                
                _l = QtGui.QHBoxLayout()
                _d = QtGui.QHBoxLayout()

                self.rssLinks[feed.entries[i].title] = feed.entries[i].link
                
                title = ClickableQLabel(feed.entries[i].title)
                self.connect(title, QtCore.SIGNAL('clicked()'), self.emitOpenArticle)
                title.setWordWrap(True)
                title.setMinimumWidth(self.parent().geometry().width()-100)
                font.setPointSize(12)
                font.setBold(True)
                title.setFont(font)
                
                desc = QtGui.QLabel("  " + feed.entries[i].description.split('<br')[0])
                desc.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
                desc.setMinimumWidth(self.parent().geometry().width()-100)
                desc.setWordWrap(True)
                font.setPointSize(10)
                font.setBold(False)
                desc.setFont(font)
                
                _l.addWidget(title)
                _d.addWidget(desc)
                _l.addStretch(1)
                _d.addStretch(1)
                
                vbox.addLayout(_l)
                vbox.addLayout(_d)
            i += 1
        return w

    def emitOpenArticle(self):
        # emit a signal so Mainwindow can open browser
        if (not self.signalsBlocked()):
            self.articleClicked.emit(self.rssLinks[self.sender().text()])
        return

    def resizeEvent(self,resizeEvent): # Resizes text to fit the width of the frame
        w = self.updateArticles()
        self.scroll.setWidget(w)

    def scrollDown(self):
        current = self.scroll.verticalScrollBar().value()
        maxScroll = self.scroll.verticalScrollBar().maximum()
        if (current+30) <= maxScroll:
            self.scroll.verticalScrollBar().setValue(current+30)
        else:
            self.scroll.verticalScrollBar().setValue(maxScroll)

    def scrollUp(self):
        current = self.scroll.verticalScrollBar().value()
        minScroll = self.scroll.verticalScrollBar().minimum()
        if (current-30) >= minScroll:
            self.scroll.verticalScrollBar().setValue(current-30)
        else:
            self.scroll.verticalScrollBar().setValue(minScroll)

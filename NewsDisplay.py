# -*- coding: utf-8 -*-
import pyowm
import feedparser
#from time import *
#from datetime import datetime
from PyQt4 import QtCore, QtGui
from WebBrowser import WebPage
from ExtendedQLabel import ClickableQLabel

class NewsWidget(QtGui.QWidget):

    def __init__(self, parent, websize):
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
        
        self.feedList = self.getFeeds()
        self.webSize = websize
        print(websize)
        
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
        self.vLay.addWidget(self.scroll)

        w = self.updateArticles()
        self.scroll.setWidget(w)
    #end def
        
    def updateUI(self):
        self.feedList = self.getFeeds() # get new feed objects
        w = self.updateArticles()
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
                self.connect(title, QtCore.SIGNAL('clicked()'), self.openArticle)
                title.setWordWrap(True)
                font.setPointSize(12)
                font.setBold(True)
                title.setFont(font)
                
                desc = QtGui.QLabel("  " + feed.entries[i].description.split('<br')[0])
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

    def openArticle(self):
        # Open a webbrowser to the article
        web = WebPage(self.window(), self.window().geometry(), self.rssLinks[self.sender().text()])
        return

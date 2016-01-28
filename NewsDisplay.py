# -*- coding: utf-8 -*-
import pyowm
import feedparser
from time import *
from datetime import datetime
from PyQt4 import QtCore, QtGui
from random import choice

class NewsWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(NewsWidget, self).__init__(parent)
        
        self.rssList = list() # contatins all rss urls
        self.feedList = list() # contains all rss feed objects
        
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
        
        for x in range(0, choice(range(5,15))):
            _l = QtGui.QHBoxLayout()
            _d = QtGui.QHBoxLayout()
            
            title = QtGui.QLabel(self.feedList[0].entries[2].title + ": ")
            font.setPointSize(12)
            font.setBold(True)
            title.setFont(font)
            
            desc = QtGui.QLabel("    " + self.feedList[0].entries[3].description.split('<br')[0])
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
            
        return w
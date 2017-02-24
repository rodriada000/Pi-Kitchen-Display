# -*- coding: utf-8 -*-
import feedparser
from time import *
from PyQt4 import QtCore, QtGui
from WebBrowser import WebPage
from ExtendedQLabel import ClickableQLabel

MAXLEN = 45 # max length of article summary
MAXSCROLL = 125 # amount to scroll every few seconds

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
        
        self.scrollTimer = QtCore.QTimer()
        self.scrollTimer.timeout.connect(self.doScroll)
        self.scrollTimer.start(15000) # timer to scroll through articles (every 15 sec)
        self.scrollDir = 'down'
        
        self.initUI()
    #end def
        
    def initUI(self):
        self.vLay = QtGui.QVBoxLayout(self)
        self.vLay.setSpacing(0)
        
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.scroll.verticalScrollBar().setStyleSheet("""QScrollBar:vertical { width: 35px; }""")
        
        font = QtGui.QFont("Arial")
        font.setItalic(True)
        font.setPointSize(8)

        self.hbox = QtGui.QHBoxLayout(self)
        
        self.updateLbl = QtGui.QLabel()
        self.updateLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignBottom)
        self.updateLbl.setMaximumWidth(100)
        self.updateLbl.setFont(font)
        
        # self.hbox.addWidget(self.updateLbl)
        
        self.vLay.addLayout(self.hbox)
        self.vLay.addWidget(self.scroll)

        self.updateUI()
    #end def
        
    def updateUI(self):
        """
        Retrieves new articles and updates the UI to display
        new articles.
        """
        self.feedList = self.getFeeds() # get new feed objects
        w = self.updateArticles() # create new widget with updated articles
        # self.updateLbl.setText(strftime("Updated at %-I:%M"))
        self.scroll.setWidget(w)
        
    def getFeeds(self):
        """
        Get a feed object for each RSS url in rssfeed.cfg and returns a list of feed objects.
        RSS Articles can be retrieved by accessing the entries list property.
        """
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
                if i >= len(feed.entries): # verify that an entry exists for feed
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
                
                try:
                    description = self.shortenSummary(feed.entries[i].summary) # shorten the description if longer than desired
                except:
                    description = ""
                
                desc = QtGui.QLabel("  " + description)
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

    def shortenSummary(self, desc_str):
        """
        Takes the RSS article summary or description as parameter and shortens it
        to MAXLEN charachters. Also strips any html from the string.
        returns new shortened string.
        """
        #TODO: update method to be more robust against all html
        desc_str = desc_str.split('<br')[0] # remove any extra html (happens on CNN rss feeds)
        descL = desc_str.split(' ') # get list of words

        if len(descL) > MAXLEN:
            return ' '.join(descL[:MAXLEN]) + '...'
        else:
            return desc_str

    def emitOpenArticle(self):
        """
        Emits a signal when an article is clicked. Used to notify
        the MainWindow to open browser with the clicked article.
        """
        if (not self.signalsBlocked()):
            self.articleClicked.emit(self.rssLinks[self.sender().text()])
        return

    def resizeEvent(self,resizeEvent): # Resizes text to fit the width of the frame
        w = self.updateArticles()
        self.scroll.setWidget(w)

    def scrollDown(self):
        """
        Automatically scroll RSS feed down a specific amount.
        """
        current = self.scroll.verticalScrollBar().value()
        maxValue = self.scroll.verticalScrollBar().maximum()

        self.animation = QtCore.QPropertyAnimation(self.scroll.verticalScrollBar(), "value")
        self.animation.setDuration(1500)
        self.animation.setStartValue(current)

        if (current+MAXSCROLL) <= maxValue:
            self.animation.setEndValue(current+MAXSCROLL)
        else:
            self.scrollDir = 'up' # reached bottom of list, scroll up now
            self.animation.setEndValue(maxValue)
        self.animation.start()

    def scrollUp(self):
        """
        Automatically scroll RSS feed up a specific amount.
        """
        current = self.scroll.verticalScrollBar().value()
        minValue = self.scroll.verticalScrollBar().minimum()

        self.animation = QtCore.QPropertyAnimation(self.scroll.verticalScrollBar(), "value")
        self.animation.setDuration(1500)
        self.animation.setStartValue(current)

        if (current-MAXSCROLL) >= minValue:
            self.animation.setEndValue(current-MAXSCROLL)
        else:
            self.scrollDir = 'down' # reached bottom of list, scroll up now
            self.animation.setEndValue(minValue)
        self.animation.start()
            
    def doScroll(self):
        """
        Function connected to scroll timer to be triggered every few seconds.
        """
        if self.scrollDir == 'down':
            self.scrollDown()
        else:
            self.scrollUp()

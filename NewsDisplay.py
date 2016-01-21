# -*- coding: utf-8 -*-
import pyowm
import feedparser
from time import *
from datetime import datetime
from PyQt4 import QtCore, QtGui

class NewsWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(NewsWidget, self).__init__(parent)
        
        self.rssList = list() # contatins all rss feed urls
        
        try:
            with open('rssfeed.cfg') as urls:
                lines = [line.rstrip('\n') for line in urls]
                for rss in lines:
                    if rss[0] == '#': continue
                    self.rssList.append(rss)
        except:
            print("Failed to open rssfeed.cfg..")
            return
        
        # for e in f.entries:
            
        #     print(e.title.encode('utf-8'))
        #     print(e.description.split('<br')[0].encode('utf-8'))
        #     print(e.published)
        #     print("")
        self.initUI()
    #end def
        
    def initUI(self):
        vLay = QtGui.QVBoxLayout(self)
        scroll = QtGui.QScrollArea()
        scroll.setWidgetResizable(True)
        vLay.addWidget(scroll)
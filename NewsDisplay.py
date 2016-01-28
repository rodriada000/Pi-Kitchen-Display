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
        vLay.setSpacing(0)
        
        scroll = QtGui.QScrollArea()
        scroll.setWidgetResizable(True)
        vLay.addWidget(scroll)
        
        w = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(w)
        
        for x in range(0, choice(range(50,150))):
            _l = QtGui.QHBoxLayout()
            _l.addWidget(QtGui.QLabel("Label # %d" % x, self))
            _l.addWidget(QtGui.QCheckBox(self))
            _l.addWidget(QtGui.QComboBox(self))
            _l.addStretch(1)
            vbox.addLayout(_l)
            
        scroll.setWidget(w)
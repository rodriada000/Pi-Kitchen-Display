# -*- coding: utf-8 -*-
import pyowm
from time import *
from datetime import datetime
from PyQt4 import QtCore, QtGui

class NewsWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(NewsWidget, self).__init__(parent)

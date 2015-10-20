# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Sat Oct 17 18:24:36 2015
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from time import strftime
from PyQt4 import QtCore, QtGui
from MusicBrowser import MusicPage
from WeatherDisplay import WeatherWidget

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(606, 391)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(606, 391))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        # Weather Display Widget
        self.frame_weather = QtGui.QFrame(self.centralwidget)
        self.frame_weather.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_weather.setFrameShadow(QtGui.QFrame.Plain)
        self.frame_weather.setObjectName(_fromUtf8("frame_weather"))
        self.gridLayout.addWidget(self.frame_weather, 0, 0, 2, 2)

        self.weather_hlay = QtGui.QHBoxLayout(self.frame_weather)
        self.weather_hlay.addWidget(WeatherWidget(self.frame_weather))


        self.frame = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(211, 150))
        self.frame.setMaximumSize(QtCore.QSize(211, 161))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout.addWidget(self.frame, 0, 2, 1, 1)
        self.label_clock = QtGui.QLabel(self.centralwidget)
        self.label_clock.setMinimumSize(QtCore.QSize(111, 41))
        self.label_clock.setMaximumSize(QtCore.QSize(211, 41))

        # Setup Clock
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Droid Sans [monotype]"))
        font.setPointSize(28)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_clock.setFont(font)
        self.label_clock.setAutoFillBackground(False)
        self.label_clock.setTextFormat(QtCore.Qt.AutoText)
        self.label_clock.setScaledContents(False)
        self.label_clock.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_clock.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_clock.setObjectName(_fromUtf8("label_clock"))
        self.label_clock.setText(strftime("%-I" + ":" + "%M"))
        self.clockTimer = QtCore.QTimer()
        self.clockTimer.timeout.connect(self.updateClock)
        self.clockTimer.start(1000)
        self.gridLayout.addWidget(self.label_clock, 1, 2, 1, 1)

        self.pushButton_internet = QtGui.QPushButton(self.centralwidget)
        self.pushButton_internet.setMinimumSize(QtCore.QSize(121, 51))
        self.pushButton_internet.setObjectName(_fromUtf8("pushButton_internet"))
        self.gridLayout.addWidget(self.pushButton_internet, 2, 0, 1, 1)
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Plain)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout.addWidget(self.frame_2, 2, 1, 2, 1)

        # Calendar Widget
        self.calendarWidget_main = QtGui.QCalendarWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendarWidget_main.sizePolicy().hasHeightForWidth())
        self.calendarWidget_main.setSizePolicy(sizePolicy)
        self.calendarWidget_main.setMinimumSize(QtCore.QSize(217, 119))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("FreeSans"))
        self.calendarWidget_main.setFont(font)
        self.calendarWidget_main.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.calendarWidget_main.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.calendarWidget_main.setVerticalHeaderFormat(QtGui.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget_main.setNavigationBarVisible(False)
        self.calendarWidget_main.setDateEditEnabled(False)
        self.calendarWidget_main.setObjectName(_fromUtf8("calendarWidget_main"))
        self.gridLayout.addWidget(self.calendarWidget_main, 2, 2, 2, 1)

        # Music Player Button
        self.pushButton_mp = QtGui.QPushButton(self.centralwidget)
        self.pushButton_mp.setMinimumSize(QtCore.QSize(121, 51))
        self.pushButton_mp.setObjectName(_fromUtf8("pushButton_mp"))
        self.pushButton_mp.clicked.connect(self.mpClick)
        self.gridLayout.addWidget(self.pushButton_mp, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        # Status Bar
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Initialize music player
        self.musicOpened = False

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_clock.setText(_translate("MainWindow", strftime("%-I" + ":" + "%M"), None))
        self.pushButton_internet.setText(_translate("MainWindow", "Web Browser", None))
        self.pushButton_mp.setText(_translate("MainWindow", "Music Player", None))

    def mpClick(self):
        # Check if music player is already opened but is hidden
        if (self.musicOpened == True and self.musicPlayer.isHidden()):
            self.musicPlayer.resize(self.centralwidget.geometry().width(), self.centralwidget.geometry().height()) # resize music player when re-opening
            self.musicPlayer.show()
        else: # Create music player if not opened yet
            self.musicPlayer = MusicPage(self.centralwidget, self.centralwidget.geometry())
            self.musicOpened = True

        self.statusbar.showMessage('Music Player Opened.')

    def updateClock(self):
        self.label_clock.setText(strftime("%-I" + ":" + "%M"))



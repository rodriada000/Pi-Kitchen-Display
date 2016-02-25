from time import *
from PyQt4 import QtCore, QtGui

class DishWasherWidget(QtGui.QWidget):

    def __init__(self, parent):
        """
            Initialize the browser GUI and connect the events
        """
        super(DishWasherWidget, self).__init__(parent)
        
        self.clean = True
        self.initUi()
    #def end
    
    def initUi(self):
        
        self.vLayout = QtGui.QVBoxLayout(self)
        self.updateBtn = QtGui.QPushButton()
        self.statusLabel = QtGui.QLabel()
        self.timeLabel = QtGui.QLabel()
        
        # Font for status
        font = QtGui.QFont()
        font.setPointSize(24) # Static size for now
        font.setBold(True)
        self.statusLabel.setFont(font)
        
        self.updateBtn.setText("Update")
        self.updateBtn.setMinimumHeight(50)
        font.setPointSize(12)
        font.setBold(False)
        self.updateBtn.setFont(font)
        self.updateBtn.clicked.connect(self.updateStatus)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.updateBtn.setSizePolicy(sizePolicy)
        
        hlay = QtGui.QHBoxLayout()
        hlay.addStretch(1)
        hlay.addWidget(self.updateBtn)
        
        self.updateStatus() # set intial text
        
        self.vLayout.addWidget(self.statusLabel)
        self.vLayout.addWidget(self.timeLabel)
        self.vLayout.addLayout(hlay)
        self.vLayout.setContentsMargins(5, 5, 5, 5)
        self.vLayout.setSpacing(1)
        
        self.show()
    #def end
    
    def updateStatus(self):
        if self.clean is True:
            self.statusLabel.setText("Dishes Dirty")
            self.clean = False
        else:
            self.statusLabel.setText("Dishes Clean")
            self.clean = True
        
        self.timeLabel.setText("Last updated " + strftime("%b %d %-I:%M"))
    #def end
    
    def resizeEvent(self,resizeEvent): # Resizes text to fit inside cell
        font = QtGui.QFont()
        
        # Resize 'dirty/clean' status label
        widg = self.vLayout.itemAt(0).widget()
        rect = self.vLayout.itemAt(0).geometry()
        
        maxSize = 24 # max font for displaying 'dirty/clean'
        size = self.bestFontSize(widg.text(), rect) # get best size for QRect
        if size > maxSize:
            size = maxSize
        font.setPointSize(size)
        widg.setFont(font)

        # Resize 'last updated' label
        maxSize = 16;
        widg = self.vLayout.itemAt(1).widget()
        rect = self.vLayout.itemAt(1).geometry()
        
        size = self.bestFontSize(widg.text(), rect) # get best size for QRect
        if size > maxSize:
            size = maxSize
        font.setPointSize(size)
        widg.setFont(font)
    #def end
    
    def bestFontSize(self, text, cellRect):
        size = 2 # minimum font size of 2
        ff = QtGui.QFont()
        ff.setPointSize(size)
        
        qf = QtGui.QFontMetrics(ff)
        
        while (True):
            textRect = qf.boundingRect(text)
            if textRect.width() > cellRect.width():
                break
            size += 1
            ff.setPointSize(size)
            qf = QtGui.QFontMetrics(ff)
            
        return size - 1 # reduce font size by 1 to fit within cellRect
    #def end

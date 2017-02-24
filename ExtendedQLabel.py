"""
module that extends QtGui.QLabel to add a mouse click event
to the QLabel.
"""
from PyQt4 import QtCore, QtGui
 
class ClickableQLabel(QtGui.QLabel):
    def __init(self, parent):
        QtGui.QLabel.__init__(self, parent)
 
    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked()'))

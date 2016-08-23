# -*- coding: utf-8 -*-

"""
Module implementing version_show.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from core.Ui_version import Ui_About_Dialog

version_number = "1.0.0"

class version_show(QDialog, Ui_About_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(version_show, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """

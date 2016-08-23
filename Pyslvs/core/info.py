# -*- coding: utf-8 -*-

"""
Module implementing Info_Dialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from core.Ui_info import Ui_Info_Dialog

class Info_show(QDialog, Ui_Info_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Info_show, self).__init__(parent)
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

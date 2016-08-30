# -*- coding: utf-8 -*-

"""
Module implementing edit_rod_show.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_edit_rod import Ui_Dialog


class edit_rod_show(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(edit_rod_show, self).__init__(parent)
        self.setupUi(self)

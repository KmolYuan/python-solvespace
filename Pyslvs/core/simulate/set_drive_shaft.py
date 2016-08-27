# -*- coding: utf-8 -*-

"""
Module implementing shaft_show.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_set_drive_shaft import Ui_Dialog

class shaft_show(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(shaft_show, self).__init__(parent)
        self.setupUi(self)

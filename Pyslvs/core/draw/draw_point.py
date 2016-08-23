# -*- coding: utf-8 -*-

"""
Module implementing New_point.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_draw_point import Ui_Dialog

class New_point(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(New_point, self).__init__(parent)
        self.setupUi(self)

# -*- coding: utf-8 -*-

"""
Module implementing edit_point_show.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_draw_edit_point import Ui_Dialog

class edit_point_show(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(edit_point_show, self).__init__(parent)
        self.setupUi(self)

# -*- coding: utf-8 -*-

"""
Module implementing edit_link_show.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_draw_edit_link import Ui_Dialog

class edit_link_show(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(edit_link_show, self).__init__(parent)
        self.setupUi(self)

# -*- coding: utf-8 -*-

"""
Module implementing edit_stay_chain_show.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_draw_edit_stay_chain import Ui_Dialog

class edit_stay_chain_show(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(edit_stay_chain_show, self).__init__(parent)
        self.setupUi(self)

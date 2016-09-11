# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_draw_point import Ui_Dialog

class New_point(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(New_point, self).__init__(parent)
        self.setupUi(self)
        #Mask
        mask = QRegExp('[n]?[1-9]{1,1}[0-9]{1,3}[.]+[0-9]{1,4}')
        self.X_coordinate.setValidator(QRegExpValidator(mask))
        self.Y_coordinate.setValidator(QRegExpValidator(mask))

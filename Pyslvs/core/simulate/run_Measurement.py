# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_run_Measurement import Ui_Form

class Measurement_show(QWidget, Ui_Form):
    point_change = pyqtSignal(int, int)
    def __init__(self, parent=None):
        super(Measurement_show, self).__init__(parent)
        self.setupUi(self)
        self.Distance.setPlainText("0.0")
    
    @pyqtSlot(float, float)
    def show_mouse_track(self, x, y): self.Mouse.setPlainText("("+str(x)+", "+str(y)+")")
    
    @pyqtSlot(int)
    def on_Start_currentIndexChanged(self, index): self.point_change.emit(self.Start.currentIndex(), self.End.currentIndex())
    @pyqtSlot(int)
    def on_End_currentIndexChanged(self, index): self.point_change.emit(self.Start.currentIndex(), self.End.currentIndex())
    
    @pyqtSlot(float)
    def change_distance(self, val): self.Distance.setPlainText(str(val))

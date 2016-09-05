# -*- coding: utf-8 -*-

"""
Module implementing Path_Track_show.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from .Ui_run_Path_Track import Ui_Dialog

class Path_Track_show(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Path_Track_show, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot()
    def on_add_button_clicked(self):
        try:
            self.Run_list.addItem(self.Point_list.currentItem().text())
            self.Point_list.takeItem(self.Point_list.currentRow())
        except: pass
    
    @pyqtSlot()
    def on_remove_botton_clicked(self):
        try:
            self.Point_list.addItem(self.Run_list.currentItem().text())
            self.Run_list.takeItem(self.Run_list.currentRow())
        except: pass

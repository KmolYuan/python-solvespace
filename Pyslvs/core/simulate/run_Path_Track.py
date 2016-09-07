# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_run_Path_Track import Ui_Dialog

from .. import calculation

class Path_Track_show(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Path_Track_show, self).__init__(parent)
        self.setupUi(self)
        self.work = WorkerThread()
        self.Path_data = []
        self.Entiteis_Point = None
        self.Entiteis_Link = None
        self.Entiteis_Stay_Chain = None
        self.Drive_Shaft = None
        self.Slider = None
        self.Rod = None
        self.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.start)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.stop)
    
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
    
    def start(self):
        self.work.Run_list = self.Run_list
        self.work.Entiteis_Point = self.Entiteis_Point
        self.work.Entiteis_Link = self.Entiteis_Link
        self.work.Entiteis_Stay_Chain = self.Entiteis_Stay_Chain
        self.work.Drive_Shaft = self.Drive_Shaft
        self.work.Slider = self.Slider
        self.work.Rod = self.Rod
        self.work.start()
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)
    
    def stop(self):
        self.work.stop()
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)

class WorkerThread(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.stoped = False
        self.mutex = QMutex()
    
    def __del__(self):
        self.exiting = True
        self.wait()
    
    def run(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
        point_list = []
        for i in range(self.Run_list.count()):
            point_list += [int(self.Run_list.item(i).text().replace("Point", ""))]
        table2 = self.Drive_Shaft
        Path = []
        solvespace = calculation.Solvespace()
        for i in range(table2.rowCount()):
            Path += [solvespace.path_process(
                float(table2.item(i, 3).text().replace("°", "")), float(table2.item(i, 4).text().replace("°", "")),
                point_list, self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Stay_Chain,
                self.Drive_Shaft, self.Slider, self.Rod)]
        self.Path_data = Path
        print(self.Path_data)
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True
    
    def isStop(self):
        with QMutexLocker(self.mutex): return self.stoped

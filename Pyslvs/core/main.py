# -*- coding: utf-8 -*-
#CSV & SQLite
import csv, math
from peewee import *
#PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
_translate = QCoreApplication.translate
#UI Ports
from .Ui_main import Ui_MainWindow
import webbrowser
#Dialog Ports
from .info.version import version_show
from .info.color import color_show
from .info.info import Info_show
from .info.help import Help_info_show
from .info.script import Script_Dialog
from .info.path_point_data import path_point_data_show
#Warning Dialog Ports
from .warning.reset_workbook import reset_show
from .warning.zero_value import zero_show
from .warning.repeated_value import same_show
from .warning.restriction_conflict import restriction_conflict_show
from .warning.kill_origin import kill_origin_show
from .warning.resolution_fail import resolution_fail_show
#Drawing Dialog Ports
from .draw.draw_point import New_point
from .draw.draw_link import New_link
from .draw.draw_stay_chain import chain_show
from .draw.draw_edit_point import edit_point_show
from .draw.draw_edit_link import edit_link_show
from .draw.draw_edit_stay_chain import edit_stay_chain_show
#Delete Dialog Ports
from .draw.draw_delete_point import delete_point_show
from .draw.draw_delete_linkage import delete_linkage_show
from .draw.draw_delete_chain import delete_chain_show
from .simulate.delete_drive_shaft import delete_shaft_show
from .simulate.delete_slider import delete_slider_show
from .simulate.delete_rod import delete_rod_show
#Simulate Dialog Ports
from .simulate.set_drive_shaft import shaft_show
from .simulate.set_slider import slider_show
from .simulate.set_rod import rod_show
from .simulate.edit_drive_shaft import edit_shaft_show
from .simulate.edit_slider import edit_slider_show
from .simulate.edit_rod import edit_rod_show
from .simulate.run_Path_Track import Path_Track_show
from .simulate.run_Drive import Drive_show
from .simulate.run_Measurement import Measurement_show
#DynamicCanvas
from .canvas import DynamicCanvas
#Solve
from .calculation import Solvespace
from .list_process import *

Environment_variables = "../"

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #No Save
        self.Workbook_Change = False
        #mpl Window
        self.qpainterWindow = DynamicCanvas()
        self.qpainterWindow.setStatusTip(_translate("MainWindow",
            "Press Ctrl Key and use mouse to Change Origin or Zoom Size."))
        self.mplLayout.insertWidget(0, self.qpainterWindow)
        self.qpainterWindow.show()
        #Script & Path
        self.Script = ""
        self.Path_data = []
        self.Path_Run_list = []
        #Entiteis_Point Right-click menu
        self.Entiteis_Point_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Entiteis_Point_Widget.customContextMenuRequested.connect(self.on_point_context_menu)
        self.popMenu_point = QMenu(self)
        self.action_point_right_click_menu_add = QAction("Add a Point", self)
        self.popMenu_point.addAction(self.action_point_right_click_menu_add)
        self.action_point_right_click_menu_edit = QAction("Edit a Point", self)
        self.popMenu_point.addAction(self.action_point_right_click_menu_edit)
        self.popMenu_point.addSeparator()
        self.action_point_right_click_menu_delete = QAction("Delete a Point", self)
        self.popMenu_point.addAction(self.action_point_right_click_menu_delete) 
        #Entiteis_Link Right-click menu
        self.Entiteis_Link_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Entiteis_Link_Widget.customContextMenuRequested.connect(self.on_link_context_menu)
        self.popMenu_link = QMenu(self)
        self.action_link_right_click_menu_add = QAction("Add a Link", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_add)
        self.action_link_right_click_menu_edit = QAction("Edit a Link", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_edit)
        self.popMenu_link.addSeparator()
        self.action_link_right_click_menu_move_up = QAction("Move up", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_move_up)
        self.action_link_right_click_menu_move_down = QAction("Move down", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_move_down)
        self.popMenu_link.addSeparator()
        self.action_link_right_click_menu_delete = QAction("Delete a Link", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_delete) 
        #Entiteis_Chain Right-click menu
        self.Entiteis_Stay_Chain_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Entiteis_Stay_Chain_Widget.customContextMenuRequested.connect(self.on_chain_context_menu)
        self.popMenu_chain = QMenu(self)
        self.action_chain_right_click_menu_add = QAction("Add a Chain", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_add)
        self.action_chain_right_click_menu_edit = QAction("Edit a Chain", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_edit)
        self.popMenu_chain.addSeparator()
        self.action_chain_right_click_menu_move_up = QAction("Move up", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_move_up)
        self.action_chain_right_click_menu_move_down = QAction("Move down", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_move_down)
        self.popMenu_chain.addSeparator()
        self.action_chain_right_click_menu_delete = QAction("Delete a Chain", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_delete) 
        #Drive_Shaft Right-click menu
        self.Drive_Shaft_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Drive_Shaft_Widget.customContextMenuRequested.connect(self.on_shaft_context_menu)
        self.popMenu_shaft = QMenu(self)
        self.action_shaft_right_click_menu_add = QAction("Add a Drive Shaft", self)
        self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_add)
        self.action_shaft_right_click_menu_edit = QAction("Edit a Drive Shaft", self)
        self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_edit)
        self.popMenu_shaft.addSeparator()
        self.action_shaft_right_click_menu_delete = QAction("Delete a Drive Shaft", self)
        self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_delete) 
        #Slider Right-click menu
        self.Slider_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Slider_Widget.customContextMenuRequested.connect(self.on_slider_context_menu)
        self.popMenu_slider = QMenu(self)
        self.action_slider_right_click_menu_add = QAction("Add a Slider", self)
        self.popMenu_slider.addAction(self.action_slider_right_click_menu_add)
        self.action_slider_right_click_menu_edit = QAction("Edit a Slider", self)
        self.popMenu_slider.addAction(self.action_slider_right_click_menu_edit)
        self.popMenu_slider.addSeparator()
        self.action_slider_right_click_menu_delete = QAction("Delete a Slider", self)
        self.popMenu_slider.addAction(self.action_slider_right_click_menu_delete) 
        #Rod Right-click menu
        self.Rod_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Rod_Widget.customContextMenuRequested.connect(self.on_rod_context_menu)
        self.popMenu_rod = QMenu(self)
        self.action_rod_right_click_menu_add = QAction("Add a Rod", self)
        self.popMenu_rod.addAction(self.action_rod_right_click_menu_add)
        self.action_rod_right_click_menu_edit = QAction("Edit a Rod", self)
        self.popMenu_rod.addAction(self.action_rod_right_click_menu_edit)
        self.popMenu_rod.addSeparator()
        self.action_rod_right_click_menu_delete = QAction("Delete a Rod", self)
        self.popMenu_rod.addAction(self.action_rod_right_click_menu_delete)
        #Resolve
        self.Resolve()
    
    #Right-click menu event
    def on_point_context_menu(self, point):
        action = self.popMenu_point.exec_(self.Entiteis_Point_Widget.mapToGlobal(point))
        if action == self.action_point_right_click_menu_add: self.on_action_New_Point_triggered()
        elif action == self.action_point_right_click_menu_edit: self.on_actionEdit_Point_triggered()
        elif action == self.action_point_right_click_menu_delete: self.on_actionDelete_Point_triggered()
    def on_link_context_menu(self, point):
        self.action_link_right_click_menu_move_up.setEnabled((not bool(self.Entiteis_Link.rowCount()<=1))and(self.Entiteis_Link.currentRow()>=1))
        self.action_link_right_click_menu_move_down.setEnabled((not bool(self.Entiteis_Link.rowCount()<=1))and(self.Entiteis_Link.currentRow()<=self.Entiteis_Link.rowCount()-2))
        action = self.popMenu_link.exec_(self.Entiteis_Link_Widget.mapToGlobal(point))
        if action == self.action_link_right_click_menu_add: self.on_action_New_Line_triggered()
        elif action == self.action_link_right_click_menu_edit: self.on_actionEdit_Linkage_triggered()
        elif action == self.action_link_right_click_menu_move_up: self.move_up(self.Entiteis_Link, self.Entiteis_Link.currentRow(), "Line")
        elif action == self.action_link_right_click_menu_move_down: self.move_down(self.Entiteis_Link, self.Entiteis_Link.currentRow(), "Line")
        elif action == self.action_link_right_click_menu_delete: self.on_actionDelete_Linkage_triggered()
    def on_chain_context_menu(self, point):
        self.action_chain_right_click_menu_move_up.setEnabled((not bool(self.Entiteis_Stay_Chain.rowCount()<=1))and(self.Entiteis_Stay_Chain.currentRow()>=1))
        self.action_chain_right_click_menu_move_down.setEnabled((not bool(self.Entiteis_Stay_Chain.rowCount()<=1))and(self.Entiteis_Stay_Chain.currentRow()<=self.Entiteis_Link.rowCount()-2))
        action = self.popMenu_chain.exec_(self.Entiteis_Stay_Chain_Widget.mapToGlobal(point))
        if action == self.action_chain_right_click_menu_add: self.on_action_New_Stay_Chain_triggered()
        elif action == self.action_chain_right_click_menu_edit: self.on_actionEdit_Stay_Chain_triggered()
        elif action == self.action_chain_right_click_menu_move_up: self.move_up(self.Entiteis_Stay_Chain, self.Entiteis_Stay_Chain.currentRow(), "Chain")
        elif action == self.action_chain_right_click_menu_move_down: self.move_down(self.Entiteis_Stay_Chain, self.Entiteis_Stay_Chain.currentRow(), "Chain")
        elif action == self.action_chain_right_click_menu_delete: self.on_actionDelete_Stay_Chain_triggered()
    def on_shaft_context_menu(self, point):
        action = self.popMenu_shaft.exec_(self.Drive_Shaft_Widget.mapToGlobal(point))
        if action == self.action_shaft_right_click_menu_add: self.on_action_Set_Drive_Shaft_triggered()
        elif action == self.action_shaft_right_click_menu_edit: self.on_action_Edit_Drive_Shaft_triggered()
        elif action == self.action_shaft_right_click_menu_delete: self.on_actionDelete_Drive_Shaft_triggered()
    def on_slider_context_menu(self, point):
        action = self.popMenu_slider.exec_(self.Slider_Widget.mapToGlobal(point))
        if action == self.action_slider_right_click_menu_add: self.on_action_Set_Slider_triggered()
        elif action == self.action_slider_right_click_menu_edit: self.on_action_Edit_Slider_triggered()
        elif action == self.action_slider_right_click_menu_delete: self.on_actionDelete_Slider_triggered()
    def on_rod_context_menu(self, point):
        action = self.popMenu_rod.exec_(self.Rod_Widget.mapToGlobal(point))
        if action == self.action_rod_right_click_menu_add: self.on_action_Set_Rod_triggered()
        elif action == self.action_rod_right_click_menu_edit: self.on_action_Edit_Piston_Spring_triggered()
        elif action == self.action_rod_right_click_menu_delete: self.on_actionDelete_Piston_Spring_triggered()
    
    #Table move up & down
    def move_up(self, table, row, name):
        try:
            table.insertRow(row-1)
            for i in range(table.columnCount()): table.setItem(row-1, i, QTableWidgetItem(table.item(row+1, i).text()))
            table.removeRow(row+1)
            for j in range(table.rowCount()): table.setItem(j, 0, QTableWidgetItem(name+str(j)))
            self.Workbook_noSave()
        except: pass
    def move_down(self, table, row, name):
        try:
            table.insertRow(row+2)
            for i in range(table.columnCount()): table.setItem(row+2, i, QTableWidgetItem(table.item(row, i).text()))
            table.removeRow(row)
            for j in range(table.rowCount()): table.setItem(j, 0, QTableWidgetItem(name+str(j)))
            self.Workbook_noSave()
        except: pass
    @pyqtSlot()
    def on_link_move_up_clicked(self):
        if (not bool(self.Entiteis_Link.rowCount()<=1))and(self.Entiteis_Link.currentRow()>=1): self.move_up(self.Entiteis_Link, self.Entiteis_Link.currentRow(), "Line")
    @pyqtSlot()
    def on_link_move_down_clicked(self):
        if (not bool(self.Entiteis_Link.rowCount()<=1))and(self.Entiteis_Link.currentRow()<=self.Entiteis_Link.rowCount()-2): self.move_down(self.Entiteis_Link, self.Entiteis_Link.currentRow(), "Line")
    @pyqtSlot()
    def on_chain_move_up_clicked(self):
        if (not bool(self.Entiteis_Stay_Chain.rowCount()<=1))and(self.Entiteis_Stay_Chain.currentRow()>=1): self.move_up(self.Entiteis_Stay_Chain, self.Entiteis_Stay_Chain.currentRow(), "Chain")
    @pyqtSlot()
    def on_chain_move_down_clicked(self):
        if (not bool(self.Entiteis_Stay_Chain.rowCount()<=1))and(self.Entiteis_Stay_Chain.currentRow()<=self.Entiteis_Stay_Chain.rowCount()-2): self.move_down(self.Entiteis_Stay_Chain, self.Entiteis_Stay_Chain.currentRow(), "Line")
    
    #Close Event
    def closeEvent(self, event):
        if self.Workbook_Change:
            reply = QMessageBox.question(self, 'Saving Message',
                "Are you sure to quit?\nAny Changes won't be saved.",
                (QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel), QMessageBox.Save)
            if reply == QMessageBox.Discard or reply == QMessageBox.Ok:
                print("Exit.")
                event.accept()
            elif reply == QMessageBox.Save:
                self.on_action_Output_Coordinate_to_Text_File_triggered()
                if not self.Workbook_Change:
                    print("Exit.")
                    event.accept()
                else: event.ignore()
        else: event.accept()
    
    #Resolve
    def Resolve(self):
        table_point = self.Entiteis_Point
        table_line = self.Entiteis_Link
        table_chain = self.Entiteis_Stay_Chain
        table_shaft = self.Drive_Shaft
        table_slider = self.Slider
        table_rod = self.Rod
        for i in range(table_line.rowCount()):
            a = int(table_line.item(i, 1).text().replace("Point", ""))
            b = int(table_line.item(i, 2).text().replace("Point", ""))
            case1 = float(table_point.item(a, 1).text())==float(table_point.item(b, 1).text())
            case2 = float(table_point.item(a, 2).text())==float(table_point.item(b, 2).text())
            if case1 and case2:
                if b == 0: table_point.setItem(a, 1, QTableWidgetItem(str(float(table_point.item(a, 1).text())+0.01)))
                else: table_point.setItem(b, 1, QTableWidgetItem(str(float(table_point.item(b, 1).text())+0.01)))
        for i in range(table_chain.rowCount()):
            a = int(table_chain.item(i, 1).text().replace("Point", ""))
            b = int(table_chain.item(i, 2).text().replace("Point", ""))
            c = int(table_chain.item(i, 3).text().replace("Point", ""))
            case1 = float(table_point.item(a, 1).text())==float(table_point.item(b, 1).text())
            case2 = float(table_point.item(a, 2).text())==float(table_point.item(b, 2).text())
            case3 = float(table_point.item(b, 1).text())==float(table_point.item(c, 1).text())
            case4 = float(table_point.item(b, 2).text())==float(table_point.item(c, 2).text())
            case5 = float(table_point.item(a, 1).text())==float(table_point.item(c, 1).text())
            case6 = float(table_point.item(a, 2).text())==float(table_point.item(c, 2).text())
            if case1 and case2:
                if b==0: table_point.setItem(a, 1, QTableWidgetItem(str(float(table_point.item(a, 1).text())+0.01)))
                else: table_point.setItem(b, 1, QTableWidgetItem(str(float(table_point.item(b, 1).text())+0.01)))
            if case3 and case4:
                if c==0: table_point.setItem(b, 2, QTableWidgetItem(str(float(table_point.item(b, 2).text())+0.01)))
                else: table_point.setItem(c, 2, QTableWidgetItem(str(float(table_point.item(c, 2).text())+0.01)))
            if case5 and case6:
                if c==0: table_point.setItem(a, 2, QTableWidgetItem(str(float(table_point.item(a, 2).text())+0.01)))
                else: table_point.setItem(c, 2, QTableWidgetItem(str(float(table_point.item(c, 2).text())+0.01)))
        #Solve
        result = []
        solvespace = Solvespace()
        fileName = self.windowTitle().replace("Pyslvs - ", "").replace("*", "").split("/")[-1].split(".")[0]
        result = solvespace.table_process(table_point, table_line, table_chain, table_shaft, table_slider, table_rod, fileName)
        self.Script = solvespace.Script
        if result==[]:
            print("Rebuild the cavanc falled.")
            dlg = resolution_fail_show()
            dlg.show()
            dlg.exec()
        else:
            for i in range(table_point.rowCount()):
                Point_setup(table_point, i, result[i*2], result[i*2+1])
            self.Reload_Canvas()
        print("Rebuild the cavanc.")
    
    #Reload Canvas
    def Reload_Canvas(self):
        self.qpainterWindow.update_figure(float(self.LineWidth.text()), float(self.PathWidth.text()),
            self.Entiteis_Point, self.Entiteis_Link,
            self.Entiteis_Stay_Chain, self.Drive_Shaft,
            self.Slider, self.Rod,
            self.Entiteis_Point_Style, self.ZoomText.toPlainText(),
            self.actionDisplay_Dimensions.isChecked(), self.action_Black_Blackground.isChecked())
    
    #Workbook Change
    def Workbook_noSave(self):
        self.Workbook_Change = True
        self.setWindowTitle(_translate("MainWindow", self.windowTitle().replace("*", "")+"*"))
    
    #Start @pyqtSlot()
    @pyqtSlot()
    def on_action_Full_Screen_triggered(self): print("Full Screen.")
    @pyqtSlot()
    def on_actionNormalmized_triggered(self): print("Normal Screen.")
    
    @pyqtSlot()
    def on_actionHow_to_use_triggered(self):
        dlg = Help_info_show()
        dlg.show()
        dlg.exec()
    @pyqtSlot()
    def on_actionColor_Settings_triggered(self):
        dlg = color_show()
        dlg.show()
        dlg.exec()
    @pyqtSlot()
    def on_Color_set_clicked(self): self.on_actionColor_Settings_triggered()
    @pyqtSlot()
    def on_action_Get_Help_triggered(self):
        print("Open http://project.mde.tw/blog/slvs-library-functions.html")
        webbrowser.open("http://project.mde.tw/blog/slvs-library-functions.html")
    @pyqtSlot()
    def on_actionGit_hub_Site_triggered(self):
        print("Open https://github.com/40323230/python-solvespace")
        webbrowser.open("https://github.com/40323230/python-solvespace")
    @pyqtSlot()
    def on_actionGithub_Wiki_triggered(self):
        print("Open https://github.com/40323230/python-solvespace/wiki")
        webbrowser.open("https://github.com/40323230/python-solvespace/wiki")
    @pyqtSlot()
    def on_action_About_Pyslvs_triggered(self):
        dlg = version_show()
        dlg.show()
        dlg.exec()
    @pyqtSlot()
    def on_action_About_Python_Solvspace_triggered(self):
        dlg = Info_show()
        dlg.show()
        dlg.exec()
    
    @pyqtSlot()
    def on_action_New_Workbook_triggered(self):
        if self.Workbook_Change:
            dlg  = reset_show()
            dlg.show()
            if dlg.exec_(): self.new_Workbook()
        else: self.new_Workbook()
    
    @pyqtSlot()
    def on_action_Load_Workbook_triggered(self):
        if self.Workbook_Change:
            warning_reset  = reset_show()
            warning_reset.show()
            if warning_reset.exec_(): self.load_Workbook()
        else: self.load_Workbook()
    
    def new_Workbook(self):
        Reset_notebook(self.Entiteis_Point, 1)
        Reset_notebook(self.Entiteis_Link, 0)
        Reset_notebook(self.Entiteis_Stay_Chain, 0)
        Reset_notebook(self.Entiteis_Point_Style, 1)
        Reset_notebook(self.Drive_Shaft, 0)
        Reset_notebook(self.Slider, 0)
        self.qpainterWindow.removePath()
        self.Resolve()
        print("Reset the workbook.")
        self.setWindowTitle(_translate("MainWindow", "Pyslvs - New Workbook"))
    def load_Workbook(self):
        Reset_notebook(self.Entiteis_Point, 1)
        Reset_notebook(self.Entiteis_Link, 0)
        Reset_notebook(self.Entiteis_Stay_Chain, 0)
        Reset_notebook(self.Entiteis_Point_Style, 1)
        Reset_notebook(self.Drive_Shaft, 0)
        Reset_notebook(self.Slider, 0)
        self.qpainterWindow.removePath()
        self.Resolve()
        print("Reset workbook.")
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open file...', Environment_variables, 'CSV File(*.csv);;Text File(*.txt)')
        if fileName:
            print("Get:"+fileName)
            data = []
            with open(fileName, newline="") as stream:
                reader = csv.reader(stream, delimiter=' ', quotechar='|')
                for row in reader:
                    data += ', '.join(row).split('\t,')
            bookmark = 0
            for i in range(4, len(data), 4):
                bookmark = i
                if data[i] == 'Next_table\t': break
                if data[i+3]=="Fixed": fixed = True
                else: fixed = False
                Points_list(self.Entiteis_Point, data[i], data[i+1], data[i+2], fixed, False)
            self.Entiteis_Point_Style.removeRow(0)
            for i in range(bookmark+1, len(data), 4):
                bookmark = i
                if data[i] == 'Next_table\t': break
                Points_style_add(self.Entiteis_Point_Style, data[i], data[i+1], data[i+2], data[i+3])
            for i in range(bookmark+1, len(data), 4):
                bookmark = i
                if data[i] == 'Next_table\t': break
                Links_list(self.Entiteis_Link, data[i], data[i+1], data[i+2], data[i+3], False)
            for i in range(bookmark+1, len(data), 7):
                bookmark = i
                if data[i] == 'Next_table\t': break
                Chain_list(self.Entiteis_Stay_Chain, data[i], data[i+1], data[i+2], data[i+3], data[i+4], data[i+5], data[i+6], False)
            for i in range(bookmark+1, len(data), 5):
                bookmark = i
                if data[i] == 'Next_table\t': break
                Shaft_list(self.Drive_Shaft, data[i], data[i+1], data[i+2], data[i+3], data[i+4], False)
            for i in range(bookmark+1, len(data), 3):
                bookmark = i
                if data[i] == 'Next_table\t': break
                Slider_list(self.Slider, data[i], data[i+1], data[i+2], False)
            for i in range(bookmark+1, len(data), 5):
                bookmark = i
                Rod_list(self.Slider, data[i], data[i+1], data[i+2], data[i+3], data[i+4], False)
            self.Workbook_Change = False
            self.setWindowTitle(_translate("MainWindow", "Pyslvs - "+fileName))
            self.Resolve()
            self.Path_data_exist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">No Path Data</span></p></body></html>"))
            self.Path_Clear.setEnabled(False)
            self.Path_coordinate.setEnabled(False)
            try:
                self.MeasurementWidget.deleteLater()
                self.Measurement.setChecked(False)
                self.Drive.setEnabled(True)
            except: pass
            try:
                self.DriveWidget.deleteLater()
                self.Drive.setChecked(False)
                self.Measurement.setEnabled(True)
            except: pass
            print("Successful Load the workbook...")
    
    @pyqtSlot()
    def on_action_Output_Coordinate_to_Text_File_triggered(self):
        print("Saving to CSV or text File...")
        if self.windowTitle()=="Pyslvs - New Workbook" or self.windowTitle()=="Pyslvs - New Workbook*":
            fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'Spreadsheet(*.csv)')
        else:
            fileName = self.windowTitle().replace("Pyslvs - ", "").replace("*", "")
        if fileName:
            fileName = fileName.replace(".csv", "")+".csv"
            with open(fileName, 'w', newline="") as stream:
                table = self.Entiteis_Point
                writer = csv.writer(stream)
                for row in range(table.rowCount()):
                    rowdata = []
                    for column in range(table.columnCount()-1):
                        item = table.item(row, column)
                        if item is not None:
                            if (item.checkState()==False) and (item.text()==''): rowdata += ["noFixedFixed"]
                            else:
                                if item.text()=='': rowdata += ["Fixed"]
                                else: rowdata += [item.text()+'\t']
                    writer.writerow(rowdata)
                CSV_notebook(writer, self.Entiteis_Point_Style, 4)
                CSV_notebook(writer, self.Entiteis_Link, 4)
                CSV_notebook(writer, self.Entiteis_Stay_Chain, 7)
                CSV_notebook(writer, self.Drive_Shaft, 6)
                CSV_notebook(writer, self.Slider, 3)
                CSV_notebook(writer, self.Rod, 5)
            print("Successful Save: "+fileName)
            self.Workbook_Change = False
            self.setWindowTitle(_translate("MainWindow", "Pyslvs - "+fileName))
    
    @pyqtSlot()
    def on_action_Output_to_S_QLite_Data_Base_triggered(self):
        print("Saving to Data Base...")
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'Data Base(*.db)')
        if fileName:
            fileName = fileName.replace(".db", "")
            fileName += ".db"
            #TODO: SQLite
    
    @pyqtSlot()
    def on_action_Output_to_Script_triggered(self):
        print("Saving to script...")
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'Python Script(*.py)')
        if fileName:
            fileName = fileName.replace(".py", "")
            if sub == "Python Script(*.py)": fileName += ".py"
            with open(fileName, 'w', newline="") as f:
                f.write(self.Script)
            print("Saved to:"+str(fileName))
    
    @pyqtSlot()
    def on_action_Output_to_Picture_triggered(self):
        print("Saving to picture...")
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'PNG file(*.png)')
        if fileName:
            fileName = fileName.replace(".png", "")
            fileName += ".png"
            pixmap = self.qpainterWindow.grab()
            pixmap.save(fileName)
            print("Saved to:"+str(fileName))
    
    @pyqtSlot()
    def on_action_New_Point_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        draw_point  = New_point()
        draw_point.Point_num.insertPlainText("Point"+str(table1.rowCount()))
        draw_point.show()
        if draw_point.exec_():
            Points_list(table1, draw_point.Point_num.toPlainText(),
                draw_point.X_coordinate.text(), draw_point.Y_coordinate.text(),
                draw_point.Fix_Point.checkState(), False)
            if draw_point.Fix_Point.checkState()==True: fix = "10"
            else: fix = "5"
            Points_style_add(table2, draw_point.Point_num.toPlainText(), "G", fix, "G")
            self.Resolve()
            self.Workbook_noSave()
    
    @pyqtSlot()
    def on_Point_add_button_clicked(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        x = self.X_coordinate.text()
        y = self.Y_coordinate.text()
        Points_list(table1, "Point"+str(table1.rowCount()), x, y, False, False)
        Points_style_add(table2, "Point"+str(table2.rowCount()), "G", "5", "G")
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionEdit_Point_triggered(self):
        table1 = self.Entiteis_Point
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            draw_point  = edit_point_show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            for i in range(1, table1.rowCount()):
                draw_point.Point.insertItem(i, icon, table1.item(i, 0).text())
            draw_point.show()
            if draw_point.exec_():
                table2 = self.Entiteis_Point_Style
                Points_list(table1, draw_point.Point.currentText(),
                    draw_point.X_coordinate.text(), draw_point.Y_coordinate.text(),
                    draw_point.Fix_Point.checkState(), True)
                Points_style_fix(table2, draw_point.Point.currentText(), draw_point.Fix_Point.checkState())
                self.Resolve()
                self.Workbook_noSave()
    
    @pyqtSlot()
    def on_action_New_Line_triggered(self):
        table1 = self.Entiteis_Point
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            draw_link  = New_link()
            for i in range(table1.rowCount()):
                draw_link.Start_Point.insertItem(i, icon, table1.item(i, 0).text())
                draw_link.End_Point.insertItem(i, icon, table1.item(i, 0).text())
            table2 = self.Entiteis_Link
            draw_link.Link_num.insertPlainText("Line"+str(table2.rowCount()))
            draw_link.show()
            if draw_link.exec_():
                a = draw_link.Start_Point.currentText()
                b = draw_link.End_Point.currentText()
                if Repeated_check(table2, a, b): self.on_action_New_Line_triggered()
                elif a == b:
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_New_Line_triggered()
                else:
                    Links_list(table2, draw_link.Link_num.toPlainText(),
                        draw_link.Start_Point.currentText(), draw_link.End_Point.currentText(),
                        draw_link.Length.text(), False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionEdit_Linkage_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        if (table2.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            icon2 = QIcon()
            icon2.addPixmap(QPixmap(":/icons/line.png"), QIcon.Normal, QIcon.Off)
            draw_link  = edit_link_show()
            for i in range(table1.rowCount()):
                draw_link.Start_Point.insertItem(i, icon1, table1.item(i, 0).text())
                draw_link.End_Point.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                draw_link.Link.insertItem(i, icon2, table2.item(i, 0).text())
            draw_link.show()
            if draw_link.exec_():
                a = draw_link.Start_Point.currentText()
                b = draw_link.End_Point.currentText()
                if a == b:
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_actionEdit_Linkage_triggered()
                else:
                    Links_list(table2, draw_link.Link.currentText(),
                        draw_link.Start_Point.currentText(),  draw_link.End_Point.currentText(),
                        draw_link.Length.text(), True)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_action_New_Stay_Chain_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
        table1 = self.Entiteis_Point
        if (table1.rowCount() <= 2):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            New_stay_chain = chain_show()
            table2 = self.Entiteis_Stay_Chain
            for i in range(table1.rowCount()):
                New_stay_chain.Point1.insertItem(i, icon, table1.item(i, 0).text())
                New_stay_chain.Point2.insertItem(i, icon, table1.item(i, 0).text())
                New_stay_chain.Point3.insertItem(i, icon, table1.item(i, 0).text())
            New_stay_chain.Chain_num.insertPlainText("Chain"+str(table2.rowCount()))
            New_stay_chain.show()
            if New_stay_chain.exec_():
                p1 = New_stay_chain.Point1.currentText()
                p2 = New_stay_chain.Point2.currentText()
                p3 = New_stay_chain.Point3.currentText()
                if (p1 == p2) | (p2 == p3) | (p1 == p3):
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_New_Stay_Chain_triggered()
                else:
                    Chain_list(table2, New_stay_chain.Chain_num.toPlainText(),
                        p1, p2, p3,
                        New_stay_chain.p1_p2.text(),
                        New_stay_chain.p2_p3.text(),
                        New_stay_chain.p1_p3.text(), False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionEdit_Stay_Chain_triggered(self):
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(":/icons/equal.png"), QIcon.Normal, QIcon.Off)
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Stay_Chain
        if (table2.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            New_stay_chain = edit_stay_chain_show()
            for i in range(table1.rowCount()):
                New_stay_chain.Point1.insertItem(i, icon1, table1.item(i, 0).text())
                New_stay_chain.Point2.insertItem(i, icon1, table1.item(i, 0).text())
                New_stay_chain.Point3.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                New_stay_chain.Chain.insertItem(i, icon2, table2.item(i, 0).text())
            New_stay_chain.show()
            if New_stay_chain.exec_():
                p1 = New_stay_chain.Point1.currentText()
                p2 = New_stay_chain.Point2.currentText()
                p3 = New_stay_chain.Point3.currentText()
                if (p1 == p2) | (p2 == p3) | (p1 == p3):
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_actionEdit_Stay_Chain_triggered()
                else:
                    Chain_list(table2, New_stay_chain.Chain.currentText(), p1, p2, p3,
                        New_stay_chain.p1_p2.text(),
                        New_stay_chain.p2_p3.text(),
                        New_stay_chain.p1_p3.text(), True)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_action_Set_Drive_Shaft_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Drive_Shaft
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = shaft_show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Shaft_Center.insertItem(i, icon, table1.item(i, 0).text())
                dlg.References.insertItem(i, icon, table1.item(i, 0).text())
            dlg.Shaft_num.insertPlainText("Shaft"+str(table2.rowCount()))
            dlg.show()
            if dlg.exec_():
                a = dlg.Shaft_Center.currentText()
                b = dlg.References.currentText()
                c = dlg.Start_Angle.text()
                d = dlg.End_Angle.text()
                if (a == b) or (c == d):
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Drive_Shaft_triggered()
                else:
                    Shaft_list(table2, dlg.Shaft_num.toPlainText(), a, b, c, d, False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_action_Edit_Drive_Shaft_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Drive_Shaft
        if (table2.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = edit_shaft_show()
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            icon2 = QIcon()
            icon2.addPixmap(QPixmap(":/icons/circle.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Shaft_Center.insertItem(i, icon1, table1.item(i, 0).text())
                dlg.References.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                dlg.Shaft.insertItem(i, icon2, table2.item(i, 0).text())
            dlg.show()
            if dlg.exec_():
                a = dlg.Shaft_Center.currentText()
                b = dlg.References.currentText()
                c = dlg.Start_Angle.text()
                d = dlg.End_Angle.text()
                if (a == b) or (c == d):
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Drive_Shaft_triggered()
                else:
                    Shaft_list(table2, dlg.Shaft.currentText(), a, b, c, d, True)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_action_Set_Slider_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        table3 = self.Slider
        if (table2.rowCount() <= 0) and (table1.rowCount() <= 2):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = slider_show()
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            icon2 = QIcon()
            icon2.addPixmap(QPixmap(":/icons/line.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Slider_Center.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                dlg.References.insertItem(i, icon2, table2.item(i, 0).text())
            dlg.Slider_num.insertPlainText("Slider"+str(table3.rowCount()))
            dlg.show()
            if dlg.exec_():
                a = dlg.Slider_Center.currentText()
                b = dlg.References.currentText()
                c = dlg.References.currentIndex()
                if (table2.item(c, 1).text()==a) or (table2.item(c, 2).text()==a):
                    dlg = restriction_conflict_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Slider_triggered()
                else:
                    Slider_list(table3, dlg.Slider_num.toPlainText(), a, b, False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_action_Edit_Slider_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        table3 = self.Slider
        if (table3.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = edit_slider_show()
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            icon2 = QIcon()
            icon2.addPixmap(QPixmap(":/icons/line.png"), QIcon.Normal, QIcon.Off)
            icon3 = QIcon()
            icon3.addPixmap(QPixmap(":/icons/pointonx.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Slider_Center.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                dlg.References.insertItem(i, icon2, table2.item(i, 0).text())
            for i in range(table3.rowCount()):
                dlg.Slider.insertItem(i, icon3, table3.item(i, 0).text())
            dlg.show()
            if dlg.exec_():
                a = dlg.Slider_Center.currentText()
                b = dlg.References.currentText()
                c = dlg.References.currentIndex()
                if (table2.item(c, 1).text()==a) or (table2.item(c, 2).text()==a):
                    dlg = restriction_conflict_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Edit_Slider_triggered()
                else:
                    Slider_list(table3, dlg.Slider.currentText(), a, b, True)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_action_Set_Rod_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Rod
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = rod_show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Start.insertItem(i, icon, table1.item(i, 0).text())
                dlg.End.insertItem(i, icon, table1.item(i, 0).text())
            dlg.Rod_num.insertPlainText("Rod"+str(table2.rowCount()))
            dlg.show()
            if dlg.exec_():
                a = dlg.Start.currentText()
                b = dlg.End.currentText()
                c = str(min(float(dlg.len1.text()), float(dlg.len2.text())))
                d = str(max(float(dlg.len1.text()), float(dlg.len2.text())))
                if a == b:
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Drive_Shaft_triggered()
                else:
                    Rod_list(table2, dlg.Rod_num.toPlainText(), a, b, c, d, False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_action_Edit_Piston_Spring_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Rod
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = edit_rod_show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Start.insertItem(i, icon, table1.item(i, 0).text())
                dlg.End.insertItem(i, icon, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                dlg.Rod.insertItem(i, icon, table2.item(i, 0).text())
            dlg.show()
            if dlg.exec_():
                a = dlg.Start.currentText()
                b = dlg.End.currentText()
                c = str(min(float(dlg.len1.text()), float(dlg.len2.text())))
                d = str(max(float(dlg.len1.text()), float(dlg.len2.text())))
                if a == b:
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Drive_Shaft_triggered()
                else:
                    Rod_list(table2, dlg.Rod.currentText(), a, b, c, d, True)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Point_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
        table = self.Entiteis_Point
        if table.rowCount() <= 1:
            dlg = kill_origin_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = delete_point_show()
            for i in range(1, table.rowCount()):
                dlg.Point.insertItem(i, icon, table.item(i, 0).text())
            dlg.show()
            if dlg.exec_():
                Point_list_delete(table,
                    self.Entiteis_Point_Style, self.Entiteis_Link,
                    self.Entiteis_Stay_Chain, self.Drive_Shaft,
                    self.Slider, self.Rod, dlg)
                self.Resolve()
                self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Linkage_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/line.png"), QIcon.Normal, QIcon.Off)
        table1 = self.Entiteis_Link
        table2 = self.Slider
        if table1.rowCount() <= 0:
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = delete_linkage_show()
            for i in range(table1.rowCount()):
                dlg.Entity.insertItem(i, icon, table1.item(i, 0).text())
            dlg.show()
            if dlg.exec_():
                Link_list_delete(table1, table2, dlg)
                self.Resolve()
                self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Stay_Chain_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/equal.png"), QIcon.Normal, QIcon.Off)
        Delete_dlg_set(self.Entiteis_Stay_Chain, delete_chain_show(), "Chain")
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Drive_Shaft_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/circle.png"), QIcon.Normal, QIcon.Off)
        Delete_dlg_set(self.Drive_Shaft, delete_shaft_show(), "Shaft")
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Slider_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/pointonx.png"), QIcon.Normal, QIcon.Off)
        Delete_dlg_set(self.Slider, icon, delete_slider_show(), "Slider")
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Piston_Spring_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/spring.png"), QIcon.Normal, QIcon.Off)
        Delete_dlg_set(self.Rod, icon, delete_rod_show(), "Rod")
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot(int)
    def on_ZoomBar_valueChanged(self, value):
        self.ZoomText.setPlainText(str(value)+"%")
        self.Reload_Canvas()
    
    def wheelEvent(self, event):
        if QApplication.keyboardModifiers()==Qt.ControlModifier:
            if event.angleDelta().y()>0: self.ZoomBar.setValue(self.ZoomBar.value()+10)
            if event.angleDelta().y()<0: self.ZoomBar.setValue(self.ZoomBar.value()-10)
    
    @pyqtSlot()
    def on_actionReload_Drawing_triggered(self): self.Resolve()
    
    @pyqtSlot(QTableWidgetItem)
    def on_Entiteis_Point_Style_itemChanged(self, item):
        self.Reload_Canvas()
        self.Workbook_noSave()
    @pyqtSlot(int)
    def on_LineWidth_valueChanged(self, p0): self.Reload_Canvas()
    @pyqtSlot(int)
    def on_PathWidth_valueChanged(self, p0): self.Reload_Canvas()
    @pyqtSlot(bool)
    def on_actionDisplay_Dimensions_toggled(self, p0): self.Reload_Canvas()
    @pyqtSlot(bool)
    def on_action_Black_Blackground_toggled(self, p0): self.Reload_Canvas()
    
    @pyqtSlot()
    def on_PathTrack_clicked(self):
        table1 = self.Entiteis_Point
        dlg = Path_Track_show()
        self.actionDisplay_Dimensions.setChecked(True)
        for i in range(table1.rowCount()):
            if not table1.item(i, 3).checkState(): dlg.Point_list.addItem(table1.item(i, 0).text())
        if dlg.Point_list.count()==0:
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg.Entiteis_Point = self.Entiteis_Point
            dlg.Entiteis_Link = self.Entiteis_Link
            dlg.Entiteis_Stay_Chain = self.Entiteis_Stay_Chain
            dlg.Drive_Shaft = self.Drive_Shaft
            dlg.Slider = self.Slider
            dlg.Rod = self.Rod
            dlg.show()
            if dlg.exec_():
                for i in range(dlg.Run_list.count()): self.Path_Run_list += [dlg.Run_list.item(i).text()]
                self.Path_data = dlg.Path_data
                self.Path_data_exist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">Path Data Exist</span></p></body></html>"))
                self.Path_Clear.setEnabled(True)
                self.Path_coordinate.setEnabled(True)
                self.qpainterWindow.path_track(dlg.Path_data)
    @pyqtSlot()
    def on_Path_Clear_clicked(self):
        self.qpainterWindow.removePath()
        self.Reload_Canvas()
        self.Path_data_exist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">No Path Data</span></p></body></html>"))
        self.Path_Clear.setEnabled(False)
        self.Path_coordinate.setEnabled(False)
    @pyqtSlot()
    def on_Path_coordinate_clicked(self):
        dlg = path_point_data_show()
        print(self.Path_Run_list)
        Path_point_setup(dlg.path_data, self.Path_data, self.Path_Run_list)
        dlg.show()
        dlg.exec()
    
    @pyqtSlot()
    def on_Drive_clicked(self):
        if self.mplLayout.count()<=2:
            self.Measurement.setEnabled(False)
            table = self.Drive_Shaft
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/circle.png"), QIcon.Normal, QIcon.Off)
            self.DriveWidget = Drive_show()
            for i in range(table.rowCount()): self.DriveWidget.Shaft.insertItem(i, icon, table.item(i, 0).text())
            self.mplLayout.insertWidget(1, self.DriveWidget)
            self.DriveWidget.Degree_change.connect(self.Change_demo_angle)
            try:
                self.DriveWidget.Degree.setValue(int(table.item(0, 5).text().replace("°", "")*100))
                self.DriveWidget.Degree.setMinimum(int(table.item(0, 3).text().replace("°", "")*100))
                self.DriveWidget.Degree.setMaximum(int(table.item(0, 4).text().replace("°", "")*100))
                self.DriveWidget.Degree_text.setPlainText(str(float(self.DriveWidget.Degree.value()/100))+"°")
            except:
                self.DriveWidget.Degree_text.setPlainText(str(float(self.DriveWidget.Degree.value()/100))+"°")
        else:
            self.Measurement.setEnabled(True)
            try: self.DriveWidget.deleteLater()
            except: pass
    @pyqtSlot(int, float)
    def Change_demo_angle(self, shaft_int, angle):
        self.Drive_Shaft.setItem(shaft_int, 5, QTableWidgetItem(str(angle)+"°"))
        self.Resolve()
    
    distance_changed = pyqtSignal(float)
    @pyqtSlot()
    def on_Measurement_clicked(self):
        if self.mplLayout.count()<=2:
            self.Drive.setEnabled(False)
            table = self.Entiteis_Point
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            self.MeasurementWidget = Measurement_show()
            for i in range(table.rowCount()):
                self.MeasurementWidget.Start.insertItem(i, icon, table.item(i, 0).text())
                self.MeasurementWidget.End.insertItem(i, icon, table.item(i, 0).text())
            self.mplLayout.insertWidget(1, self.MeasurementWidget)
            self.actionDisplay_Dimensions.setChecked(True)
            self.qpainterWindow.mouse_track.connect(self.MeasurementWidget.show_mouse_track)
            self.MeasurementWidget.point_change.connect(self.distance_solving)
            self.distance_changed.connect(self.MeasurementWidget.change_distance)
            self.MeasurementWidget.Mouse.setPlainText("Detecting")
        else:
            self.Drive.setEnabled(True)
            try: self.MeasurementWidget.deleteLater()
            except: pass
    @pyqtSlot(int, int)
    def distance_solving(self, start, end):
        start = self.Entiteis_Point.item(start, 4).text().replace("(", "").replace(")", "")
        end = self.Entiteis_Point.item(end, 4).text().replace("(", "").replace(")", "")
        x = float(start.split(", ")[0])-float(end.split(", ")[0])
        y = float(start.split(", ")[1])-float(end.split(", ")[1])
        self.distance_changed.emit(round(math.sqrt(x**2+y**2), 9))
    
    @pyqtSlot()
    def on_action_See_Python_Scripts_triggered(self):
        dlg = Script_Dialog()
        dlg.script.setPlainText(self.Script)
        dlg.show()
        dlg.exec()

def CSV_notebook(writer, table, k):
    writer.writerow(["Next_table\t"])
    for row in range(table.rowCount()):
        rowdata = []
        for column in range(table.columnCount()):
            print(row, column)
            item = table.item(row, column)
            if item is not None:
                if column==k-1: rowdata += [item.text()]
                else: rowdata += [item.text()+'\t']
        writer.writerow(rowdata)

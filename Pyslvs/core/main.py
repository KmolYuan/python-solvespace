# -*- coding: utf-8 -*-
#CSV & SQLite
import csv
from peewee import *
#Matplotlib
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QMenu, QAction
from PyQt5.QtGui import QPixmap, QIcon
#UI Ports
from core.Ui_main import Ui_MainWindow
import webbrowser
#Preferences Setting
#from .options.Preference import Preference_show
#Dialog Ports
from .info.version import version_show
from .info.color import color_show
from .info.info import Info_show
from .info.help import Help_info_show
#Warning Dialog Ports
from .warning.reset_workbook import reset_show
from .warning.zero_value import zero_show
from .warning.repeated_value import same_show
from .warning.restriction_conflict import restriction_conflict_show
from .warning.kill_origin import kill_origin_show
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
#Solve
from .calculation import table_process

Environment_variables = "../"

class DynamicMplCanvas(FigureCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(True)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    
    def compute_initial_figure(self):
        self.axes.plot([0, 0], [-10, 10], 'b')
        self.axes.plot([-10, 10], [0, 0], 'b')
        self.axes.plot([0], [0], 'ro')
    
    def clear_figure(self):
        self.axes.clear()
    
    def update_figure(self, table_point, table_line, table_chain):
        Xval = []
        Yval = []
        for i in range(table_point.rowCount()):
            Xval += [float(table_point.item(i, 1).text())]
            Yval += [float(table_point.item(i, 2).text())]
        self.axes.plot(Xval, Yval, 'go')
        for i in range(table_line.rowCount()):
            startX = float(table_point.item(int(table_line.item(i, 1).text().replace("Point", "")), 1).text())
            startY = float(table_point.item(int(table_line.item(i, 1).text().replace("Point", "")), 2).text())
            endX = float(table_point.item(int(table_line.item(i, 2).text().replace("Point", "")), 1).text())
            endY = float(table_point.item(int(table_line.item(i, 2).text().replace("Point", "")), 2).text())
            self.axes.plot([startX, endX], [startY, endY], 'r')
        for i in range(table_chain.rowCount()):
            paX = float(table_point.item(int(table_chain.item(i, 1).text().replace("Point", "")), 1).text())
            paY = float(table_point.item(int(table_chain.item(i, 1).text().replace("Point", "")), 2).text())
            pbX = float(table_point.item(int(table_chain.item(i, 2).text().replace("Point", "")), 1).text())
            pbY = float(table_point.item(int(table_chain.item(i, 2).text().replace("Point", "")), 2).text())
            pcX = float(table_point.item(int(table_chain.item(i, 3).text().replace("Point", "")), 1).text())
            pcY = float(table_point.item(int(table_chain.item(i, 3).text().replace("Point", "")), 2).text())
            self.axes.plot([paX, pbX, pcX, paX], [paY, pbY, pcY, paY], 'r')
        self.axes.plot([0], [0], 'ro')
        self.draw()
        self.axes.set_xlabel("X Coordinate", fontsize=12)
        self.axes.set_ylabel("Y Coordinate", fontsize=12)
        a = max(max(Xval), max(Yval))+10
        b = min(min(Xval), min(Yval))-10
        self.axes.set_xlim([b, a])
        self.axes.set_ylim([b, a])

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #mpl Window
        self.mplWindow = DynamicMplCanvas()
        self.mplLayout.addWidget(self.mplWindow)
        #Entiteis_Point Right-click menu
        self.Entiteis_Point.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Entiteis_Point.customContextMenuRequested.connect(self.on_point_context_menu)
        self.popMenu_point = QMenu(self)
        self.action_point_right_click_menu_add = QAction("Add a Point", self)
        self.popMenu_point.addAction(self.action_point_right_click_menu_add)
        self.action_point_right_click_menu_edit = QAction("Edit a Point", self)
        self.popMenu_point.addAction(self.action_point_right_click_menu_edit)
        self.popMenu_point.addSeparator()
        self.action_point_right_click_menu_delete = QAction("Delete a Point", self)
        self.popMenu_point.addAction(self.action_point_right_click_menu_delete) 
        #Entiteis_Link Right-click menu
        self.Entiteis_Link.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Entiteis_Link.customContextMenuRequested.connect(self.on_link_context_menu)
        self.popMenu_link = QMenu(self)
        self.action_link_right_click_menu_add = QAction("Add a Link", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_add)
        self.action_link_right_click_menu_edit = QAction("Edit a Link", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_edit)
        self.popMenu_link.addSeparator()
        self.action_link_right_click_menu_delete = QAction("Delete a Link", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_delete) 
        #Entiteis_Chain Right-click menu
        self.Entiteis_Stay_Chain.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Entiteis_Stay_Chain.customContextMenuRequested.connect(self.on_chain_context_menu)
        self.popMenu_chain = QMenu(self)
        self.action_chain_right_click_menu_add = QAction("Add a Chain", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_add)
        self.action_chain_right_click_menu_edit = QAction("Edit a Chain", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_edit)
        self.popMenu_chain.addSeparator()
        self.action_chain_right_click_menu_delete = QAction("Delete a Chain", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_delete) 
        #Drive_Shaft Right-click menu
        self.Drive_Shaft.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Drive_Shaft.customContextMenuRequested.connect(self.on_shaft_context_menu)
        self.popMenu_shaft = QMenu(self)
        self.action_shaft_right_click_menu_add = QAction("Add a Drive Shaft", self)
        self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_add)
        self.action_shaft_right_click_menu_edit = QAction("Edit a Drive Shaft", self)
        self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_edit)
        self.popMenu_shaft.addSeparator()
        self.action_shaft_right_click_menu_delete = QAction("Delete a Drive Shaft", self)
        self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_delete) 
        #Slider Right-click menu
        self.Slider.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Slider.customContextMenuRequested.connect(self.on_slider_context_menu)
        self.popMenu_slider = QMenu(self)
        self.action_slider_right_click_menu_add = QAction("Add a Slider", self)
        self.popMenu_slider.addAction(self.action_slider_right_click_menu_add)
        self.action_slider_right_click_menu_edit = QAction("Edit a Slider", self)
        self.popMenu_slider.addAction(self.action_slider_right_click_menu_edit)
        self.popMenu_slider.addSeparator()
        self.action_slider_right_click_menu_delete = QAction("Delete a Slider", self)
        self.popMenu_slider.addAction(self.action_slider_right_click_menu_delete) 
        #Rod Right-click menu
        self.Rod.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Rod.customContextMenuRequested.connect(self.on_rod_context_menu)
        self.popMenu_rod = QMenu(self)
        self.action_rod_right_click_menu_add = QAction("Add a Rod", self)
        self.popMenu_rod.addAction(self.action_rod_right_click_menu_add)
        self.action_rod_right_click_menu_edit = QAction("Edit a Rod", self)
        self.popMenu_rod.addAction(self.action_rod_right_click_menu_edit)
        self.popMenu_rod.addSeparator()
        self.action_rod_right_click_menu_delete = QAction("Delete a Rod", self)
        self.popMenu_rod.addAction(self.action_rod_right_click_menu_delete) 
    
    #Right-click menu event
    def on_point_context_menu(self, point):
        action = self.popMenu_point.exec_(self.Entiteis_Point.mapToGlobal(point))
        if action == self.action_point_right_click_menu_add: self.on_action_New_Point_triggered()
        elif action == self.action_point_right_click_menu_edit: self.on_actionEdit_Point_triggered()
        elif action == self.action_point_right_click_menu_delete: self.on_actionDelete_Point_triggered()
    def on_link_context_menu(self, point):
        action = self.popMenu_link.exec_(self.Entiteis_Link.mapToGlobal(point))
        if action == self.action_link_right_click_menu_add: self.on_action_New_Line_triggered()
        elif action == self.action_link_right_click_menu_edit: self.on_actionEdit_Linkage_triggered()
        elif action == self.action_link_right_click_menu_delete: self.on_actionDelete_Linkage_triggered()
    def on_chain_context_menu(self, point):
        action = self.popMenu_chain.exec_(self.Entiteis_Stay_Chain.mapToGlobal(point))
        if action == self.action_chain_right_click_menu_add: self.on_action_New_Stay_Chain_triggered()
        elif action == self.action_chain_right_click_menu_edit: self.on_actionEdit_Stay_Chain_triggered()
        elif action == self.action_chain_right_click_menu_delete: self.on_actionDelete_Stay_Chain_triggered()
    def on_shaft_context_menu(self, point):
        action = self.popMenu_shaft.exec_(self.Drive_Shaft.mapToGlobal(point))
        if action == self.action_shaft_right_click_menu_add: self.on_action_Set_Drive_Shaft_triggered()
        elif action == self.action_shaft_right_click_menu_edit: self.on_action_Edit_Drive_Shaft_triggered()
        elif action == self.action_shaft_right_click_menu_delete: self.on_actionDelete_Drive_Shaft_triggered()
    def on_slider_context_menu(self, point):
        action = self.popMenu_slider.exec_(self.Slider.mapToGlobal(point))
        if action == self.action_slider_right_click_menu_add: self.on_action_Set_Slider_triggered()
        elif action == self.action_slider_right_click_menu_edit: self.on_action_Edit_Slider_triggered()
        elif action == self.action_slider_right_click_menu_delete: self.on_actionDelete_Slider_triggered()
    def on_rod_context_menu(self, point):
        action = self.popMenu_rod.exec_(self.Rod.mapToGlobal(point))
        if action == self.action_rod_right_click_menu_add: self.on_action_Set_Rod_triggered()
        elif action == self.action_rod_right_click_menu_edit: self.on_action_Edit_Piston_Spring_triggered()
        elif action == self.action_rod_right_click_menu_delete: self.on_actionDelete_Piston_Spring_triggered()
    
    #Close Event
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?\nAny Changes won't be saved.",
            QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("Exit.")
            event.accept()
        else: event.ignore()
    
    #Reload Canvas
    def Reload_Canvas(self):
        table_point = self.Entiteis_Point
        table_line = self.Entiteis_Link
        table_chain = self.Entiteis_Stay_Chain
        table_shaft = self.Drive_Shaft
        table_slider = self.Slider
        table_rod = self.Rod
        #TODO: Reload Check
        for i in range(table_line.rowCount()):
            a = int(table_line.item(i, 1).text().replace("Point", ""))
            b = int(table_line.item(i, 2).text().replace("Point", ""))
            if (table_point.item(a, 1).text()==table_point.item(b, 1).text())and(table_point.item(a, 2).text()==table_point.item(b, 2).text()):
                if b == 0: table_point.setItem(a, 1, QTableWidgetItem(str(float(table_point.item(a, 1).text())+0.01)))
                else: table_point.setItem(b, 1, QTableWidgetItem(str(float(table_point.item(b, 1).text())+0.01)))
        for i in range(table_chain.rowCount()):
            a = int(table_chain.item(i, 1).text().replace("Point", ""))
            b = int(table_chain.item(i, 2).text().replace("Point", ""))
            c = int(table_chain.item(i, 3).text().replace("Point", ""))
            case1 = (table_point.item(a, 1).text()==table_point.item(b, 1).text())
            case2 = (table_point.item(a, 2).text()==table_point.item(b, 2).text())
            case3 = (table_point.item(b, 1).text()==table_point.item(c, 1).text())
            case4 = (table_point.item(b, 2).text()==table_point.item(c, 2).text())
            case5 = (table_point.item(a, 1).text()==table_point.item(c, 1).text())
            case6 = (table_point.item(a, 2).text()==table_point.item(c, 2).text())
            if case1 and case2:
                if b ==0: table_point.setItem(a, 1, QTableWidgetItem(str(float(table_point.item(a, 1).text())+0.01)))
                else: table_point.setItem(b, 1, QTableWidgetItem(str(float(table_point.item(b, 1).text())+0.01)))
            if case3 and case4:
                if c ==0: table_point.setItem(b, 2, QTableWidgetItem(str(float(table_point.item(b, 2).text())+0.01)))
                else: table_point.setItem(c, 2, QTableWidgetItem(str(float(table_point.item(c, 2).text())+0.01)))
            if case5 and case6:
                if c ==0: table_point.setItem(a, 2, QTableWidgetItem(str(float(table_point.item(a, 2).text())+0.01)))
                else: table_point.setItem(c, 2, QTableWidgetItem(str(float(table_point.item(c, 2).text())+0.01)))
        #Solve
        result = []
        result = table_process(table_point, table_line, table_chain, table_shaft, table_slider, table_rod)
        print(result)
        if result==[]:
            print("Rebuild the cavanc falled.")
        else:
            for i in range(1, table_point.rowCount()):
                Points_list(table_point, "Point"+str(i), str(result[i*2]), str(result[i*2+1]), not(table_point.item(i, 3).checkState()==False), True)
            self.mplWindow.clear_figure()
            self.mplWindow.update_figure(table_point, table_line, table_chain)
            print("Rebuild the cavanc.")
        #TODO: Reload
    
    #Start @pyqtSlot()
    @pyqtSlot()
    def on_actionMi_nimized_triggered(self): print("Minmized Windows.")
    @pyqtSlot()
    def on_actionM_axmized_triggered(self): print("Maxmized Windows.")
    @pyqtSlot()
    def on_action_Full_Screen_triggered(self): print("Full Screen.")
    @pyqtSlot()
    def on_actionNormalmized_triggered(self): print("Normal Screen.")
    
    @pyqtSlot()
    def on_actionHow_to_use_triggered(self):
        dlg_help = Help_info_show()
        dlg_help.show()
        if dlg_help.exec_(): pass
    
    @pyqtSlot()
    def on_actionColor_Settings_triggered(self):
        dlg_color = color_show()
        dlg_color.show()
        if dlg_color.exec_(): pass
    
    @pyqtSlot()
    def on_Color_set_clicked(self):
        dlg_color = color_show()
        dlg_color.show()
        if dlg_color.exec_(): pass
    
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
        dlg_version  = version_show()
        dlg_version.show()
        if dlg_version.exec_(): pass
    
    @pyqtSlot()
    def on_action_About_Python_Solvspace_triggered(self):
        dlg_info  = Info_show()
        dlg_info.show()
        if dlg_info.exec_(): pass
    
    @pyqtSlot()
    def on_action_New_Workbook_triggered(self):
        dlg  = reset_show()
        dlg.show()
        if dlg.exec_():
            Reset_notebook(self.Entiteis_Point, 1)
            Reset_notebook(self.Entiteis_Link, 0)
            Reset_notebook(self.Entiteis_Stay_Chain, 0)
            Reset_notebook(self.Entiteis_Point_Style, 0)
            Reset_notebook(self.Drive_Shaft, 0)
            Reset_notebook(self.Slider, 0)
            self.Reload_Canvas()
            print("Reset the workbook.")
    
    @pyqtSlot()
    def on_action_Load_Workbook_triggered(self):
        warning_reset  = reset_show()
        warning_reset.show()
        if warning_reset.exec_():
            Reset_notebook(self.Entiteis_Point, 1)
            Reset_notebook(self.Entiteis_Link, 0)
            Reset_notebook(self.Entiteis_Stay_Chain, 0)
            Reset_notebook(self.Entiteis_Point_Style, 0)
            Reset_notebook(self.Drive_Shaft, 0)
            Reset_notebook(self.Slider, 0)
            self.Reload_Canvas()
            print("Reset workbook.")
            fileName, _ = QFileDialog.getOpenFileName(self, 'Open file...', Environment_variables, 'CSV File(*.csv);;Text File(*.txt)')
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
                Slider_list(self.Slider, data[i], data[i+1], data[i+2], False)
            for i in range(bookmark+1, len(data), 5):
                Rod_list(self.Slider, data[i], data[i+1], data[i+2], data[i+3], data[i+4], False)
            print("Successful Load the workbook...")
    
    @pyqtSlot()
    def on_action_Output_Coordinate_to_Text_File_triggered(self):
        print("Saving to CSV or text File...")
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'Spreadsheet(*.csv);;Text File(*.txt)')
        if fileName:
            fileName = fileName.replace(".txt", "").replace(".csv", "")
            if sub == "Text File(*.txt)": fileName += ".txt"
            if sub == "CSV File(*.csv)": fileName += ".csv"
            with open(fileName, 'w', newline="") as stream:
                table = self.Entiteis_Point
                writer = csv.writer(stream)
                for row in range(table.rowCount()):
                    rowdata = []
                    for column in range(table.columnCount()):
                        print(row, column)
                        item = table.item(row, column)
                        if item is not None:
                            if (item.checkState()==False) and (item.text()==''): rowdata += ["noFixed"]
                            else:
                                if item.text()=='': rowdata += ["Fixed"]
                                else: rowdata += [item.text()+'\t']
                    writer.writerow(rowdata)
                CSV_notebook(writer, self.Entiteis_Point_Style)
                CSV_notebook(writer, self.Entiteis_Link)
                CSV_notebook(writer, self.Entiteis_Stay_Chain)
                CSV_notebook(writer, self.Drive_Shaft)
                CSV_notebook(writer, self.Slider)
                CSV_notebook(writer, self.Rod)
    
    @pyqtSlot()
    def on_action_Output_to_S_QLite_Data_Base_triggered(self):
        print("Saving to CSV or text File...")
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'Data Base(*.db)')
        if fileName:
            fileName = fileName.replace(".db", "")
            fileName += ".db"
            with sqlite3.connect(fileName) as conn:
                conn.execute('''CREATE TABLE POINT_COORDINATES
                    (ID INT PRIMARY KEY     NOT NULL,
                    NAME           TEXT    NOT NULL,
                    X            FLOAT     NOT NULL,
                    Y            FLOAT     NOT NULL);''')
                for row in range():
                    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
                VALUES (1, 'Paul', 32, 'California', 20000.00 )")
            #TODO: SQLite
    
    @pyqtSlot()
    def on_action_Output_to_Script_triggered(self):
        print("Saving to script...")
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'Python Script(*.py)')
        if fileName:
            fileName = fileName.replace(".py", "")
            if sub == "Python Script(*.py)": fileName += ".py"
            print("Saved to:"+str(fileName))
            # TODO: Output_to_Script
    
    @pyqtSlot()
    def on_action_Output_to_Picture_triggered(self):
        print("Saving to picture...")
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'PNG file(*.png)')
        if fileName:
            fileName = fileName.replace(".png", "")
            if sub == "PNG file(*.png)": fileName += ".png"
            pixmap = self.mplWindow.grab()
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
            Points_style_add(table2, draw_point.Point_num.toPlainText(), "GREEN", "1", "GREEN")
    
    @pyqtSlot()
    def on_Point_add_button_clicked(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        x = self.X_coordinate.text()
        y = self.Y_coordinate.text()
        Points_list(table1, "Point"+str(table1.rowCount()), x, y, False, False)
        Points_style_add(table2, "Point"+str(table2.rowCount()), "GREEN", "1", "GREEN")
    
    @pyqtSlot()
    def on_actionEdit_Point_triggered(self):
        table = self.Entiteis_Point
        if (table.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            if dlg.exec_(): pass
        else:
            draw_point  = edit_point_show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            for i in range(1, table.rowCount()):
                draw_point.Point.insertItem(i, icon, table.item(i, 0).text())
            draw_point.show()
            if draw_point.exec_():
                Points_list(table, draw_point.Point.currentText(),
                    draw_point.X_coordinate.text(), draw_point.Y_coordinate.text(),
                    draw_point.Fix_Point.checkState(), True)
    
    @pyqtSlot()
    def on_action_New_Line_triggered(self):
        table1 = self.Entiteis_Point
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            if dlg.exec_(): pass
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
                if a == b:
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_New_Line_triggered()
                else:
                    Links_list(table2, draw_link.Link_num.toPlainText(),
                        draw_link.Start_Point.currentText(), draw_link.End_Point.currentText(),
                        draw_link.Length.text(), False)
    
    @pyqtSlot()
    def on_actionEdit_Linkage_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        if (table2.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            if dlg.exec_(): pass
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
    
    @pyqtSlot()
    def on_action_New_Stay_Chain_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
        table1 = self.Entiteis_Point
        if (table1.rowCount() <= 2):
            dlg = zero_show()
            dlg.show()
            if dlg.exec_(): pass
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
            if dlg.exec_(): pass
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
    
    @pyqtSlot()
    def on_action_Set_Drive_Shaft_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Drive_Shaft
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            if dlg.exec_(): pass
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
    
    @pyqtSlot()
    def on_action_Edit_Drive_Shaft_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Drive_Shaft
        if (table2.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            if dlg.exec_(): pass
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
    
    @pyqtSlot()
    def on_action_Set_Slider_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        table3 = self.Slider
        if (table2.rowCount() <= 0) and (table1.rowCount() <= 2):
            dlg = zero_show()
            dlg.show()
            if dlg.exec_(): pass
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
    
    @pyqtSlot()
    def on_action_Edit_Slider_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        table3 = self.Slider
        if (table3.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            if dlg.exec_(): pass
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
    
    @pyqtSlot()
    def on_action_Set_Rod_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Rod
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            if dlg.exec_(): pass
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
    
    @pyqtSlot()
    def on_action_Edit_Piston_Spring_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Rod
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            if dlg.exec_(): pass
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
    
    @pyqtSlot()
    def on_actionDelete_Point_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        table3 = self.Entiteis_Link
        table4 = self.Entiteis_Stay_Chain
        if table1.rowCount() <= 1:
            dlg = kill_origin_show()
            dlg.show()
            if dlg.exec_(): pass
        else:
            dlg = delete_point_show()
            for i in range(1, table1.rowCount()):
                dlg.Point.insertItem(i, icon, table1.item(i, 0).text())
            dlg.show()
            if dlg.exec_(): Point_list_delete(table1, table2, table3, table4, dlg)
    
    @pyqtSlot()
    def on_actionDelete_Linkage_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/line.png"), QIcon.Normal, QIcon.Off)
        Delete_dlg_set(self.Entiteis_Link, icon, delete_linkage_show(), "Line")
    
    @pyqtSlot()
    def on_actionDelete_Stay_Chain_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/equal.png"), QIcon.Normal, QIcon.Off)
        Delete_dlg_set(self.Entiteis_Stay_Chain, delete_chain_show(), "Chain")
    
    @pyqtSlot()
    def on_actionDelete_Drive_Shaft_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/circle.png"), QIcon.Normal, QIcon.Off)
        Delete_dlg_set(self.Drive_Shaft, delete_shaft_show(), "Shaft")
    
    @pyqtSlot()
    def on_actionDelete_Slider_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/pointonx.png"), QIcon.Normal, QIcon.Off)
        Delete_dlg_set(self.Slider, icon, delete_slider_show(), "Slider")
    
    @pyqtSlot()
    def on_actionDelete_Piston_Spring_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/spring.png"), QIcon.Normal, QIcon.Off)
        Delete_dlg_set(self.Rod, icon, delete_rod_show(), "Rod")
    
    @pyqtSlot()
    def on_Reload_Button_clicked(self): self.Reload_Canvas()
    
    @pyqtSlot()
    def on_actionReload_Drawing_triggered(self): self.Reload_Canvas()

def Points_list(table, name, x, y, fixed, edit):
    rowPosition = int(name.replace("Point", ""))
    if not edit: table.insertRow(rowPosition)
    name_set = QTableWidgetItem(name)
    name_set.setFlags(Qt.ItemIsEnabled)
    table.setItem(rowPosition, 0, name_set)
    table.setItem(rowPosition, 1, QTableWidgetItem(x))
    table.setItem(rowPosition, 2, QTableWidgetItem(y))
    checkbox = QTableWidgetItem("")
    checkbox.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    if fixed: checkbox.setCheckState(Qt.Checked)
    else: checkbox.setCheckState(Qt.Unchecked)
    table.setItem(rowPosition, 3, checkbox)
    if not edit: print("Add Point"+str(rowPosition)+".")
    else: print("Edit Point"+str(rowPosition)+".")

def Links_list(table, name, start, end, l, edit, ):
    rowPosition = int(name.replace("Line", ""))
    if not edit: table.insertRow(rowPosition)
    name_set = QTableWidgetItem(name)
    name_set.setFlags(Qt.ItemIsEnabled)
    table.setItem(rowPosition, 0, name_set)
    table.setItem(rowPosition, 1, QTableWidgetItem(start))
    table.setItem(rowPosition, 2, QTableWidgetItem(end))
    table.setItem(rowPosition, 3, QTableWidgetItem(l))
    if not edit: print("Add a link, Line "+str(rowPosition)+".")
    else: print("Edit a link, Line "+str(rowPosition)+".")

def Chain_list(table, name, p1, p2, p3, a, b, c, edit, ):
    rowPosition = int(name.replace("Chain", ""))
    if not edit: table.insertRow(rowPosition)
    name_set = QTableWidgetItem(name)
    name_set.setFlags(Qt.ItemIsEnabled)
    table.setItem(rowPosition, 0, name_set)
    table.setItem(rowPosition, 1, QTableWidgetItem(p1))
    table.setItem(rowPosition, 2, QTableWidgetItem(p2))
    table.setItem(rowPosition, 3, QTableWidgetItem(p3))
    table.setItem(rowPosition, 4, QTableWidgetItem(a))
    table.setItem(rowPosition, 5, QTableWidgetItem(b))
    table.setItem(rowPosition, 6, QTableWidgetItem(c))
    if not edit: print("Add a Triangle Chain, Line "+str(rowPosition)+".")
    else: print("Edit a Triangle Chain, Line "+str(rowPosition)+".")

def Shaft_list(table, name, center, references, start, end, edit, ):
    rowPosition = int(name.replace("Shaft", ""))
    name_set = QTableWidgetItem(name)
    name_set.setFlags(Qt.ItemIsEnabled)
    if not edit: table.insertRow(rowPosition)
    table.setItem(rowPosition, 0, name_set)
    table.setItem(rowPosition, 1, QTableWidgetItem(center))
    table.setItem(rowPosition, 2, QTableWidgetItem(references))
    table.setItem(rowPosition, 3, QTableWidgetItem(start))
    table.setItem(rowPosition, 4, QTableWidgetItem(end))
    if not edit: print("Set the Point to new Shaft.")
    else: print("Set the Point to selected Shaft.")

def Slider_list(table, name, center, references, edit, ):
    rowPosition = int(name.replace("Slider", ""))
    name_set = QTableWidgetItem(name)
    name_set.setFlags(Qt.ItemIsEnabled)
    if not edit: table.insertRow(rowPosition)
    table.setItem(rowPosition, 0, name_set)
    table.setItem(rowPosition, 1, QTableWidgetItem(center))
    table.setItem(rowPosition, 2, QTableWidgetItem(references))
    if not edit: print("Set the Point to new Slider.")
    else: print("Set the Point to selected Slider.")

def Rod_list(table, name, start, end, min, max, edit, ):
    rowPosition = int(name.replace("Rod", ""))
    name_set = QTableWidgetItem(name)
    name_set.setFlags(Qt.ItemIsEnabled)
    if not edit: table.insertRow(rowPosition)
    table.setItem(rowPosition, 0, name_set)
    table.setItem(rowPosition, 1, QTableWidgetItem(start))
    table.setItem(rowPosition, 2, QTableWidgetItem(end))
    table.setItem(rowPosition, 3, QTableWidgetItem(min))
    table.setItem(rowPosition, 4, QTableWidgetItem(max))
    if not edit: print("Set the Point to new Rod.")
    else: print("Set the Point to selected Rod.")

def Points_style_add(table, name, color, ringsize, ringcolor, ):
    rowPosition = table.rowCount()
    table.insertRow(rowPosition)
    name_set = QTableWidgetItem(name)
    name_set.setFlags(Qt.ItemIsEnabled)
    table.setItem(rowPosition, 0, name_set)
    table.setItem(rowPosition, 1, QTableWidgetItem(color))
    table.setItem(rowPosition, 2, QTableWidgetItem(ringsize))
    table.setItem(rowPosition, 3, QTableWidgetItem(ringcolor))
    print("Add Point Style for Point"+str(rowPosition)+".")

def Point_list_delete(table1, table2, table3, table4, dlg, ):
    for i in range(table3.rowCount()):
        if (dlg.Point.currentText() == table3.item(i, 1).text()) or (dlg.Point.currentText() == table3.item(i, 2).text()):
            table3.removeRow(i)
            for j in range(i, table3.rowCount()): table3.setItem(j, 0, QTableWidgetItem("Line"+str(j)))
            break
    for i in range(table4.rowCount()):
        if (dlg.Point.currentText() == table4.item(i, 1).text()) or (dlg.Point.currentText() == table4.item(i, 2).text()):
            table4.removeRow(i)
            for j in range(i, table4.rowCount): table4.setItem(j, 0, QTableWidgetItem("Chain"+str(j)))
            break
    for i in range(1, table1.rowCount()):
        if (dlg.Point.currentText() == table1.item(i, 0).text()):
            table1.removeRow(i)
            table2.removeRow(i)
            for j in range(i, table1.rowCount()): table1.setItem(j, 0, QTableWidgetItem("Point"+str(j)))
            for j in range(i, table1.rowCount()): table2.setItem(j, 0, QTableWidgetItem("Point"+str(j)))
            break

def One_list_delete(table, name, dlg, ):
    for i in range(table.rowCount()):
        if (dlg.Entity.currentText() == table.item(i, 0).text()):
            table.removeRow(i)
            for j in range(i, table.rowCount()): table.setItem(j, 0, QTableWidgetItem(name+str(j)))
            break

def Delete_dlg_set(table, icon, dlg, name):
    if table.rowCount() <= 0:
        dlg = zero_show()
        dlg.show()
        if dlg.exec_(): pass
    else:
        for i in range(table.rowCount()):
            dlg.Entity.insertItem(i, icon, table.item(i, 0).text())
        dlg.show()
        if dlg.exec_(): One_list_delete(table, name, dlg)

def Reset_notebook(table, k):
    for i in reversed(range(k, table.rowCount())): table.removeRow(i)

def CSV_notebook(writer, table):
    writer.writerow(["Next_table\t"])
    for row in range(table.rowCount()):
        rowdata = []
        for column in range(table.columnCount()):
            print(row, column)
            item = table.item(row, column)
            if item is not None:
                rowdata += [item.text()+'\t']
        writer.writerow(rowdata)

# -*- coding: utf-8 -*-
#MainWindow.
import csv
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
#UI Ports
from core.Ui_main import Ui_MainWindow
import webbrowser
#Dialog Ports
from .version import version_show
from .info import Info_show
from .warning.reset_workbook import reset_show
from .warning.zero_value import zero_show
from .warning.repeated_value import same_show
from .draw.draw_point import New_point
from .draw.draw_link import New_link
from .draw.draw_stay_chain import chain_show
from .draw.draw_delete_point import delete_point_show
#from .python_solve import Solve

Environment_variables = '../'

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        """
        Constructor
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?\nAny Changes won't be saved.",
            QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("Exit.")
            event.accept()
        else:
            event.ignore()
    
    @pyqtSlot()
    def on_actionMi_nimized_triggered(self):
        print("Minmized Windows.")
    
    @pyqtSlot()
    def on_actionM_axmized_triggered(self):
        print("Maxmized Windows.")
    
    @pyqtSlot()
    def on_action_Full_Screen_triggered(self):
        print("Full Screen.")
    
    @pyqtSlot()
    def on_actionNormalmized_triggered(self):
        print("Normal Screen.")
    
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
        if dlg_version.exec_():
            pass
    
    @pyqtSlot()
    def on_action_About_Python_Solvspace_triggered(self):
        dlg_info  = Info_show()
        dlg_info.show()
        if dlg_info.exec_():
            pass
    
    @pyqtSlot()
    def on_action_New_Workbook_triggered(self):
        dlg  = reset_show()
        dlg.show()
        if dlg.exec_():
            table1 = self.Entiteis_Point
            table2 = self.Entiteis_Link
            table3 = self.Entiteis_Stay_Chain
            for i in reversed(range(1, table1.rowCount())):
                table1.removeRow(i)
            for i in reversed(range(table2.rowCount())):
                table2.removeRow(i)
            for i in reversed(range(table3.rowCount())):
                table3.removeRow(i)
            print("Reset workbook.")
    
    @pyqtSlot()
    def on_action_Load_Workbook_triggered(self):
        warning_reset  = reset_show()
        warning_reset.show()
        if warning_reset.exec_():
            table1 = self.Entiteis_Point
            table2 = self.Entiteis_Link
            table3 = self.Entiteis_Stay_Chain
            for i in reversed(range(1, table1.rowCount())):
                table1.removeRow(i)
            for i in reversed(range(table2.rowCount())):
                table2.removeRow(i)
            for i in reversed(range(table3.rowCount())):
                table3.removeRow(i)
            print("Reset workbook.")
            print("Loading workbook...")
            fileName, _ = QFileDialog.getOpenFileName(self, 'Open file...', Environment_variables, 'Python Script(*.py)')
            print("Get:"+str(fileName))
            #TODO: Load Workbook
    
    @pyqtSlot()
    def on_action_Output_to_Script_triggered(self):
        print("Saving to script...")
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'Python Script(*.py)')
        if sub == "Python Script(*.py)":
            fileName += ".py"
        print("Saved to:"+str(fileName))
        # TODO: Output_to_Script
    
    @pyqtSlot()
    def on_action_Output_to_Picture_triggered(self):
        print("Saving to script...")
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'PNG file(*.png)')
        if sub == "PNG file(*.png)":
            fileName += ".png"
        print("Saved to:"+str(fileName))
        # TODO: Output_to_Picture
    
    @pyqtSlot()
    def on_action_Output_Coordinate_to_Text_File_triggered(self):
        table = self.Entiteis_Point
        print("Saving to script...")
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'Text File(*.txt);;CSV File(*.csv)')
        if fileName:
            fileName = fileName.replace(".txt", "")
            fileName = fileName.replace(".csv", "")
            if sub == "Text File(*.txt)":
                fileName += ".txt"
            if sub == "CSV File(*.csv)":
                fileName += ".csv"
            stream = open(fileName, 'w', newline="\n")
            writer = csv.writer(stream)
            csv.register_dialect(
                'mydialect',
                delimiter = ',',
                quotechar = '\"',
                doublequote = True,
                skipinitialspace = True,
                lineterminator = '\r\n',
                quoting = csv.QUOTE_MINIMAL)
            for row in range(table.rowCount()):
                rowdata = []
                for column in range(table.columnCount()):
                    print(row, column)
                    item = table.item(row, column)
                    if item is not None:
                        rowdata += [item.text()+'\t']
                    else:
                        rowdata += ['\n']
                writer.writerow(rowdata)
    
    @pyqtSlot()
    def on_action_New_Point_triggered(self):
        table = self.Entiteis_Point
        draw_point  = New_point()
        draw_point.Point_num.insertPlainText("Point"+str(table.rowCount()))
        draw_point.show()
        if draw_point.exec_():
            x = draw_point.X_coordinate.text()
            y = draw_point.Y_coordinate.text()
            fixed = draw_point.Fix_Point.checkState()
            Points_list_add(table, x, y, fixed)
    
    @pyqtSlot()
    def on_Point_add_button_clicked(self):
        table = self.Entiteis_Point
        x = self.X_coordinate.text()
        y = self.Y_coordinate.text()
        Points_list_add(table, x, y, False)
    
    @pyqtSlot()
    def on_action_New_Line_triggered(self):
        table1 = self.Entiteis_Point
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            if dlg.exec_():
                pass
        else:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            draw_link  = New_link()
            for i in range(table1.rowCount()):
                point_select = "Point"+str(i)
                draw_link.Start_Piont.insertItem(i, icon, point_select)
                draw_link.End_Point.insertItem(i, icon, point_select)
            table2 = self.Entiteis_Link
            draw_link.Link_num.insertPlainText("Line"+str(table2.rowCount()))
            draw_link.show()
            if draw_link.exec_():
                a = draw_link.Start_Piont.currentText()
                b = draw_link.End_Point.currentText()
                if a == b:
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_():
                        pass
                else:
                    start = draw_link.Start_Piont.currentText()
                    end = draw_link.Start_Piont.currentText()
                    l = draw_link.Length.text()
                    Links_list_add(table2, start, end, l)
    
    @pyqtSlot()
    def on_action_New_Stay_Chain_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/equal.png"), QIcon.Normal, QIcon.Off)
        table1 = self.Entiteis_Point
        if (table1.rowCount() <= 2):
            dlg = zero_show()
            dlg.show()
            if dlg.exec_():
                pass
        else:
            New_stay_chain = chain_show()
            table2 = self.Entiteis_Stay_Chain
            for i in range(table1.rowCount()):
                point_select = "Point"+str(i)
                New_stay_chain.Point1.insertItem(i, icon, point_select)
                New_stay_chain.Point2.insertItem(i, icon, point_select)
                New_stay_chain.Point3.insertItem(i, icon, point_select)
            New_stay_chain.Chain_num.insertPlainText("Chain"+str(table2.rowCount()))
            New_stay_chain.show()
            if New_stay_chain.exec_():
                p1 = New_stay_chain.Point1.currentText()
                p2 = New_stay_chain.Point2.currentText()
                p3 = New_stay_chain.Point3.currentText()
                if (p1 == p2) | (p2 == p3) | (p1 == p3):
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_():
                        pass
                else:
                    a = New_stay_chain.p1_p2.text()
                    b = New_stay_chain.p2_p3.text()
                    c = New_stay_chain.p1_p3.text()
                    Chain_list_add(table2, p1, p2, p3, a, b, c)
    
    @pyqtSlot()
    def on_actionDelet_Entity_triggered(self):
        table = self.Entiteis_Point
        if table.rowCount() <= 1:
            dlg = zero_show()
            dlg.show()
            if dlg.exec_():
                pass
        else:
            dlg = delete_point_show()
            dlg.show
            if dlg.exec_():
                pass

def Points_list_add(table, x, y, fixed):
    rowPosition = table.rowCount()
    table.insertRow(rowPosition)
    table.setItem(rowPosition , 0, QTableWidgetItem("Point"+str(rowPosition)))
    table.setItem(rowPosition , 1, QTableWidgetItem(str(x)))
    table.setItem(rowPosition , 2, QTableWidgetItem(str(y)))
    checkbox = QTableWidgetItem("")
    checkbox.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    if fixed:
        checkbox.setCheckState(Qt.Checked)
    else:
        checkbox.setCheckState(Qt.Unchecked)
    table.setItem(rowPosition , 3, checkbox)
    print("Add Point"+str(rowPosition)+".")

def Links_list_add(table, start, end, l):
    rowPosition = table.rowCount()
    table.insertRow(rowPosition)
    table.setItem(rowPosition , 0, QTableWidgetItem("Line "+str(rowPosition)))
    table.setItem(rowPosition , 1, QTableWidgetItem(str(start)))
    table.setItem(rowPosition , 2, QTableWidgetItem(str(end)))
    table.setItem(rowPosition , 3, QTableWidgetItem(str(l)))
    print("Add a link, Line "+str(rowPosition)+".")

def Chain_list_add(table, p1, p2, p3, a, b, c):
    rowPosition = table.rowCount()
    table.insertRow(rowPosition)
    table.setItem(rowPosition , 0, QTableWidgetItem("Chain "+str(rowPosition)))
    table.setItem(rowPosition , 1, QTableWidgetItem(str(p1)))
    table.setItem(rowPosition , 2, QTableWidgetItem(str(p2)))
    table.setItem(rowPosition , 3, QTableWidgetItem(str(p3)))
    table.setItem(rowPosition , 4, QTableWidgetItem(str(a)))
    table.setItem(rowPosition , 5, QTableWidgetItem(str(b)))
    table.setItem(rowPosition , 6, QTableWidgetItem(str(c)))
    print("Add a Triangle Chain, Line "+str(rowPosition)+".")

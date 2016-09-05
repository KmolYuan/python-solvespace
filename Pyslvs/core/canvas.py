# -*- coding: utf-8 -*-
#PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class DynamicCanvas(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setParent(parent)
        self.setMouseTracking(True)
        self.Reset_Origin = False
        self.Xval = []
        self.Yval = []
        self.Blackground = Qt.white
        self.origin_x = 200
        self.origin_y = 250
        self.drag = False
        self.Dimension = False
        self.Path = []
        self.pen_width = 2
        self.re_Color = [
            'R', 'G', 'B', 'C', 'M', 'Y', 'Gy', 'Og', 'Pk',
            'Bk', 'W',
            'DR', 'DG', 'DB', 'DC', 'DM', 'DY', 'DGy', 'DOg', 'DPk']
        val_Color = [
            Qt.red, Qt.green, Qt.blue, Qt.cyan, Qt.magenta, Qt.yellow, Qt.gray, QColor(225, 165, 0), QColor(225, 192, 230),
            Qt.black, Qt.white,
            Qt.darkRed, Qt.darkGreen, Qt.darkBlue, Qt.darkMagenta, Qt.darkCyan, Qt.darkYellow, Qt.darkGray, QColor(225, 140, 0), QColor(225, 20, 147)]
        self.Color = dict(zip(self.re_Color, val_Color))
    
    def update_figure(self, width,
            table_point, table_line,
            table_chain, table_shaft,
            table_slider, table_rod,
            table_style, zoom_rate,
            Dimension, Blackground):
        if Blackground: self.Blackground = Qt.black
        else: self.Blackground = Qt.white
        self.Dimension = Dimension
        self.pen_width = width
        self.Xval = []
        self.Yval = []
        self.zoom = float(zoom_rate.replace("%", ""))/100
        self.rate_all = 2
        for i in range(table_point.rowCount()):
            self.Xval += [float(table_point.item(i, 1).text())*self.zoom*self.rate_all]
            self.Yval += [float(table_point.item(i, 2).text())*self.zoom*self.rate_all*(-1)]
        self.table_point = table_point
        self.table_line = table_line
        self.table_chain = table_chain
        self.table_shaft = table_shaft
        self.table_slider = table_slider
        self.table_rod = table_rod
        self.table_style = table_style
        self.update()
    
    def path_track(self, path):
        self.Path = path
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(self.Blackground))
        painter.translate(self.origin_x, self.origin_y)
        for i in range(self.table_chain.rowCount()):
            pa = int(self.table_chain.item(i, 1).text().replace("Point", ""))
            pb = int(self.table_chain.item(i, 2).text().replace("Point", ""))
            pc = int(self.table_chain.item(i, 3).text().replace("Point", ""))
            pen = QPen()
            pen.setWidth(self.pen_width)
            painter.setBrush(Qt.cyan)
            painter.drawPolygon(
                QPointF(self.Xval[pa], self.Yval[pa]),
                QPointF(self.Xval[pb], self.Yval[pb]),
                QPointF(self.Xval[pc], self.Yval[pc]), fillRule=Qt.OddEvenFill)
            painter.setBrush(Qt.NoBrush)
            if self.Dimension:
                pen.setColor(Qt.darkGray)
                painter.setPen(pen)
                mp = QPointF((self.Xval[pa]+self.Xval[pb])/2, (self.Yval[pa]+self.Yval[pb])/2)
                painter.drawText(mp, self.table_chain.item(i, 4).text())
                mp = QPointF((self.Xval[pb]+self.Xval[pc])/2, (self.Yval[pb]+self.Yval[pc])/2)
                painter.drawText(mp, self.table_chain.item(i, 5).text())
                mp = QPointF((self.Xval[pa]+self.Xval[pc])/2, (self.Yval[pa]+self.Yval[pc])/2)
                painter.drawText(mp, self.table_chain.item(i, 6).text())
        for i in range(self.table_line.rowCount()):
            start = int(self.table_line.item(i, 1).text().replace("Point", ""))
            end = int(self.table_line.item(i, 2).text().replace("Point", ""))
            point_start = QPointF(self.Xval[start], self.Yval[start])
            point_end = QPointF(self.Xval[end], self.Yval[end])
            pen = QPen()
            pen.setWidth(self.pen_width)
            pen.setColor(Qt.darkGray)
            painter.setPen(pen)
            painter.drawLine(point_start, point_end)
            if self.Dimension:
                pen.setColor(Qt.darkGray)
                painter.setPen(pen)
                mp = QPointF((self.Xval[start]+self.Xval[end])/2, (self.Yval[start]+self.Yval[end])/2)
                painter.drawText(mp, self.table_line.item(i, 3).text())
        for i in range(self.table_point.rowCount()):
            pen = QPen()
            pen.setWidth(2)
            point_center = QPointF(int(self.Xval[i]), int(self.Yval[i]))
            try: pen.setColor(self.Color[self.table_style.item(i, 1).text()])
            except KeyError: pen.setColor(Qt.green)
            painter.setPen(pen)
            painter.drawPoint(point_center)
            try: pen.setColor(self.Color[self.table_style.item(i, 3).text()])
            except KeyError: pen.setColor(Qt.green)
            painter.setPen(pen)
            r = float(self.table_style.item(i, 2).text())
            painter.drawEllipse(point_center, r, r)
            if self.Dimension:
                pen.setColor(Qt.darkGray)
                painter.setPen(pen)
                painter.drawText(point_center, "["+self.table_point.item(i, 0).text()+"]")
        if self.Path:
            print(self.Path)
            for i in range(0, len(self.Path), 2):
                X_path = self.Path[i]
                Y_path = self.Path[i+1]
                for j in range(len(X_path)-1):
                    pen.setColor(Qt.darkGray)
                    pen.setWidth(5)
                    painter.setPen(pen)
                    point_center = QPointF(X_path[j]*self.zoom*self.rate_all,
                        Y_path[j]*self.zoom*self.rate_all*(-1))
                    painter.drawPoint(point_center)
        painter.end()
    
    def mousePressEvent(self, event):
        if QApplication.keyboardModifiers()==Qt.ControlModifier: self.drag = True
    def mouseReleaseEvent(self, event): self.drag = False
    def mouseDoubleClickEvent(self, event):
        if QApplication.keyboardModifiers()==Qt.ControlModifier:
            self.origin_x = event.x()
            self.origin_y = event.y()
            self.update()
    def mouseMoveEvent(self, event):
        if self.drag:
            self.origin_x = event.x()
            self.origin_y = event.y()
            self.update()

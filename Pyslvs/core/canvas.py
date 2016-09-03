import sys
#PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
#matplotlib
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

if "-mpl" not in sys.argv:
    class DynamicCanvas(QWidget):
        def __init__(self, parent=None):
            QWidget.__init__(self, parent)
            self.setParent(parent)
            self.setMouseTracking(True)
            self.Reset_Origin = False
            self.Xval = []
            self.Yval = []
            self.origin_x = 200
            self.origin_y = 250
            self.drag = False
        
        def update_figure(self, table_point, table_line,
            table_chain, table_shaft,
            table_slider, table_rod,
            table_style, zoom_rate):
            self.Xval = []
            self.Yval = []
            zoom = float(zoom_rate.replace("%", ""))/100
            rate_all = 2
            for i in range(table_point.rowCount()):
                self.Xval += [float(table_point.item(i, 1).text())*zoom*rate_all]
                self.Yval += [float(table_point.item(i, 2).text())*zoom*rate_all*(-1)]
            self.table_point = table_point
            self.table_line = table_line
            self.table_chain = table_chain
            self.table_shaft = table_shaft
            self.table_slider = table_slider
            self.table_rod = table_rod
            self.table_style = table_style
            self.update()
        
        def paintEvent(self, event):
            #self.table_point.item(self.table_point.rowCount()-1, 0).text()
            painter = QPainter()
            painter.begin(self)
            painter.fillRect(event.rect(), QBrush(Qt.white))
            painter.translate(self.origin_x, self.origin_y)
            for i in range(self.table_chain.rowCount()):
                pa = int(self.table_chain.item(i, 1).text().replace("Point", ""))
                pb = int(self.table_chain.item(i, 2).text().replace("Point", ""))
                pc = int(self.table_chain.item(i, 3).text().replace("Point", ""))
                painter.setBrush(Qt.cyan)
                painter.drawPolygon(
                    QPointF(self.Xval[pa], self.Yval[pa]),
                    QPointF(self.Xval[pb], self.Yval[pb]),
                    QPointF(self.Xval[pc], self.Yval[pc]), fillRule=Qt.OddEvenFill)
                painter.setBrush(Qt.NoBrush)
            for i in range(self.table_line.rowCount()):
                start = int(self.table_line.item(i, 1).text().replace("Point", ""))
                end = int(self.table_line.item(i, 2).text().replace("Point", ""))
                point_start = QPointF(self.Xval[start], self.Yval[start])
                point_end = QPointF(self.Xval[end], self.Yval[end])
                pen = QPen()
                pen.setWidth(3)
                pen.setColor(Qt.darkGray)
                painter.setPen(pen)
                painter.drawLine(point_start, point_end)
            for i in range(self.table_point.rowCount()):
                pen = QPen()
                pen.setWidth(3)
                point_center = QPointF(int(self.Xval[i]), int(self.Yval[i]))
                if self.table_style.item(i, 1).text()=="R": pen.setColor(Qt.red)
                if self.table_style.item(i, 1).text()=="G": pen.setColor(Qt.darkGreen)
                if self.table_style.item(i, 1).text()=="B": pen.setColor(Qt.blue)
                if self.table_style.item(i, 1).text()=="Og": pen.setColor(QColor(255, 136, 0))
                painter.setPen(pen)
                painter.drawPoint(point_center)
                if self.table_style.item(i, 3).text()=="R": pen.setColor(Qt.red)
                if self.table_style.item(i, 3).text()=="G": pen.setColor(Qt.darkGreen)
                if self.table_style.item(i, 3).text()=="B": pen.setColor(Qt.blue)
                if self.table_style.item(i, 3).text()=="Og": pen.setColor(QColor(255, 136, 0))
                r = float(self.table_style.item(i, 2).text())
                painter.drawEllipse(point_center, r, r)
            painter.end()
        
        def mousePressEvent(self, event):
            if QApplication.keyboardModifiers()==Qt.ControlModifier: self.drag = True
        def mouseReleaseEvent(self, event): self.drag = False
        def mouseMoveEvent(self, event):
            if self.drag:
                self.origin_x = event.x()
                self.origin_y = event.y()
                self.update()
else:
    class DynamicCanvas(FigureCanvas):
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
        
        def update_figure(self, table_point, table_line,
            table_chain, table_shaft,
            table_slider, table_rod,
            table_style, zoom_rate):
            #zoom = float(zoom_rate.replace("%", ""))
            self.axes.clear()
            Xval = []
            Yval = []
            for i in range(table_point.rowCount()):
                Xval += [float(table_point.item(i, 1).text())]
                Yval += [float(table_point.item(i, 2).text())]
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
            for i in range(table_style.rowCount()):
                paX = float(table_point.item(int(table_style.item(i, 0).text().replace("Point", "")), 1).text())
                paY = float(table_point.item(int(table_style.item(i, 0).text().replace("Point", "")), 2).text())
                if table_style.item(i, 1).text()=="R": self.axes.plot(paX, paY, 'ro')
                if table_style.item(i, 1).text()=="G": self.axes.plot(paX, paY, 'go')
                if table_style.item(i, 1).text()=="B": self.axes.plot(paX, paY, 'bo')
            self.axes.plot([0], [0], 'ro')
            self.draw()
            self.axes.set_xlabel("X Coordinate", fontsize=12)
            self.axes.set_ylabel("Y Coordinate", fontsize=12)
            a = max(max(Xval), max(Yval))+10
            b = min(min(Xval), min(Yval))-10
            self.axes.set_xlim([b, a])
            self.axes.set_ylim([b, a])

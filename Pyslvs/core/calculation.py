# -*- coding: utf-8 -*-
from .slvs import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Solvespace():
    def __init__(self):
        self.Script = ""
    
    def table_process(self, table_point, table_line, table_chain, table_shaft, table_slider, table_rod, filename):
        sys = System(1000)
        #Pre-oder
        p0 = sys.add_param(0.0)
        p1 = sys.add_param(0.0)
        p2 = sys.add_param(0.0)
        Point0 = Point3d(p0, p1, p2)
        qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
        p3 = sys.add_param(qw)
        p4 = sys.add_param(qx)
        p5 = sys.add_param(qy)
        p6 = sys.add_param(qz)
        Normal1 = Normal3d(p3, p4, p5, p6)
        Workplane1 = Workplane(Point0, Normal1)
        p7 = sys.add_param(0.0)
        p8 = sys.add_param(0.0)
        Point1 = Point2d(Workplane1, p7, p8)
        Constraint.dragged(Workplane1, Point1)
        self.Script += """# -*- coding: utf-8 -*-
'''This Code is Generate by Pyslvs.'''
from slvs import *
import matplotlib.pyplot as plt

#Please Choose Point number.
Point_num = 2
wx = Point_num*2+5
wy = Point_num*2+6

def """+filename.replace(" ", "_")+"""(degree):
    sys = System(1000)
    p0 = sys.add_param(0.0)
    p1 = sys.add_param(0.0)
    p2 = sys.add_param(0.0)
    Point0 = Point3d(p0, p1, p2)
    qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
    p3 = sys.add_param(qw)
    p4 = sys.add_param(qx)
    p5 = sys.add_param(qy)
    p6 = sys.add_param(qz)
    Normal1 = Normal3d(p3, p4, p5, p6)
    Workplane1 = Workplane(Point0, Normal1)
    if degree >= 180:
        other = -1
    else:
        other = 1

    p7 = sys.add_param(0.0)
    p8 = sys.add_param(0.0)
    Point1 = Point2d(Workplane1, p7, p8)
    Constraint.dragged(Workplane1, Point1)
"""
        Point = [Point1]
        #Load tables to constraint
        for i in range(1, table_point.rowCount()):
            if not(table_shaft.rowCount()>=1):
                x = sys.add_param(float(table_point.item(i, 1).text()))
                y = sys.add_param(float(table_point.item(i, 2).text()))
            else:
                for j in range(table_shaft.rowCount()):
                    case = table_shaft.item(j, 2).text()==table_point.item(i, 0).text()
                    if case and(table_shaft.item(j, 5) is not None):
                        angle = float(table_shaft.item(j, 5).text().replace("°", ""))
                        if angle >= 180: other = -1
                        else: other = 1
                        a = int(table_shaft.item(j, 1).text().replace("Point", ""))
                        x = sys.add_param(float(table_point.item(a, 1).text()))
                        y = sys.add_param(float(table_point.item(i, 2).text())*other)
                    else:
                        x = sys.add_param(float(table_point.item(i, 1).text()))
                        y = sys.add_param(float(table_point.item(i, 2).text()))
            p = Point2d(Workplane1, x, y)
            Point += [p]
            for j in range(table_shaft.rowCount()):
                if table_shaft.item(j, 2).text()==table_point.item(i, 0).text(): self.Script += """    p"""+str(i*2+7)+""" = sys.add_param("""+str(float(table_point.item(i, 1).text()))+""")
    p"""+str(i*2+8)+""" = sys.add_param("""+str(float(table_point.item(i, 2).text()))+"""*other)
"""
                else: self.Script += """    p"""+str(i*2+7)+""" = sys.add_param("""+str(float(table_point.item(i, 1).text()))+""")
    p"""+str(i*2+8)+""" = sys.add_param("""+str(float(table_point.item(i, 2).text()))+""")
"""
            self.Script += """    Point"""+str(i+1)+""" = Point2d(Workplane1, p"""+str(i*2+7)+""", p"""+str(i*2+8)+""")
"""
            if table_point.item(i, 3).checkState():
                Constraint.dragged(Workplane1, p)
                self.Script += """    Constraint.dragged(Workplane1, Point"""+str(i+1)+""")
"""
        for i in range(table_chain.rowCount()):
            pa = int(table_chain.item(i, 1).text().replace("Point", ""))
            pb = int(table_chain.item(i, 2).text().replace("Point", ""))
            pc = int(table_chain.item(i, 3).text().replace("Point", ""))
            lenab = float(table_chain.item(i, 4).text())
            lenbc = float(table_chain.item(i, 5).text())
            lenac = float(table_chain.item(i, 6).text())
            Constraint.distance(lenab, Workplane1, Point[pa], Point[pb])
            Constraint.distance(lenbc, Workplane1, Point[pb], Point[pc])
            Constraint.distance(lenac, Workplane1, Point[pa], Point[pc])
            self.Script += """    Constraint.distance("""+str(lenab)+""", Workplane1, Point"""+str(pa+1)+""", Point"""+str(pb+1)+""")
    Constraint.distance("""+str(lenbc)+""", Workplane1, Point"""+str(pb+1)+""", Point"""+str(pc+1)+""")
    Constraint.distance("""+str(lenac)+""", Workplane1, Point"""+str(pa+1)+""", Point"""+str(pc+1)+""")
"""
        
        for i in range(table_line.rowCount()):
            start = int(table_line.item(i, 1).text().replace("Point", ""))
            end = int(table_line.item(i, 2).text().replace("Point", ""))
            len = float(table_line.item(i, 3).text())
            Constraint.distance(len, Workplane1, Point[start], Point[end])
            self.Script += """    Constraint.distance("""+str(len)+""", Workplane1, Point"""+str(start+1)+""", Point"""+str(end+1)+""")
"""
        for i in range(table_slider.rowCount()):
            pt = int(table_slider.item(i, 1).text().replace("Point", ""))
            start = int(table_line.item(int(table_slider.item(i, 2).text().replace("Line", "")), 1).text().replace("Point", ""))
            end = int(table_line.item(int(table_slider.item(i, 2).text().replace("Line", "")), 2).text().replace("Point", ""))
            line = LineSegment2d(Workplane1, Point[start], Point[end])
            Constraint.on(Workplane1, Point[pt], line)
            self.Script += """    Constraint.on(Workplane1, Point"""+str(pt+1)+""", LineSegment2d(Workplane1, Point"""+str(start+1)+""", Point"""+str(end+1)+""")
"""
        if table_shaft.rowCount() >= 1:
            pN = sys.add_param(10)
            pNN = sys.add_param(0.0)
            PointN = Point2d(Workplane1, pN, pNN)
            Point += [PointN]
            Constraint.dragged(Workplane1, Point[-1])
            Line0 = LineSegment2d(Workplane1, Point[0], Point[-1])
            self.Script += """    px = sys.add_param(10)
    py = sys.add_param(0.0)
    PointN = Point2d(Workplane1, px, py)
    Constraint.dragged(Workplane1, PointN)
    Line0 = LineSegment2d(Workplane1, Point1, PointN)
"""
            for i in range(table_shaft.rowCount()):
                center = int(table_shaft.item(i, 1).text().replace("Point", ""))
                reference = int(table_shaft.item(i, 2).text().replace("Point", ""))
                line = LineSegment2d(Workplane1, Point[center], Point[reference])
                if table_shaft.item(i, 5) is not None:
                    angle = float(table_shaft.item(i, 5).text().replace("°", ""))
                    Constraint.angle(Workplane1, angle, line, Line0, False)
                self.Script += """    Line1 = LineSegment2d(Workplane1, Point"""+str(center+1)+""", Point"""+str(reference+1)+""")
    Constraint.angle(Workplane1, degree, Line1, Line0, False)
    
    sys.solve()
    if (sys.result == SLVS_RESULT_OKAY):
        x = sys.get_param(wx).val
        y = sys.get_param(wy).val
        return x, y

if __name__=="__main__":
    Xval  = []
    Yval  = []
    for i in range(0, 361, 1):
        x, y = """+filename.replace(" ", "_")+"""(i)
        Xval += [x]
        Yval += [y]
    print("Solve Completed")
    plt.plot(Xval, Yval)
    plt.show()
"""
        sys.solve()
        result = []
        if (sys.result == SLVS_RESULT_OKAY):
            for i in range(table_point.rowCount()*2):
                result += [sys.get_param(i+7).val]
        elif (sys.result == SLVS_RESULT_INCONSISTENT): print ("SLVS_RESULT_INCONSISTENT")
        elif (sys.result == SLVS_RESULT_DIDNT_CONVERGE): print ("SLVS_RESULT_DIDNT_CONVERGE")
        elif (sys.result == SLVS_RESULT_TOO_MANY_UNKNOWNS): print ("SLVS_RESULT_TOO_MANY_UNKNOWNS")
        return result

    def Solve(self, point_int, angle, table_point, table_line, table_chain, table_shaft, table_slider, table_rod):
        sys = System(1000)
        #Pre-oder
        p0 = sys.add_param(0.0)
        p1 = sys.add_param(0.0)
        p2 = sys.add_param(0.0)
        Point0 = Point3d(p0, p1, p2)
        qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
        p3 = sys.add_param(qw)
        p4 = sys.add_param(qx)
        p5 = sys.add_param(qy)
        p6 = sys.add_param(qz)
        Normal1 = Normal3d(p3, p4, p5, p6)
        Workplane1 = Workplane(Point0, Normal1)
        p7 = sys.add_param(0.0)
        p8 = sys.add_param(0.0)
        Point1 = Point2d(Workplane1, p7, p8)
        Constraint.dragged(Workplane1, Point1)
        p9 = sys.add_param(10)
        p10 = sys.add_param(0.0)
        Point2 = Point2d(Workplane1, p9, p10)
        Constraint.dragged(Workplane1, Point2)
        Line0 = LineSegment2d(Workplane1, Point1, Point2)
        Point = [Point1]
        #Load tables to constraint
        for i in range(1, table_point.rowCount()):
            for j in range(table_shaft.rowCount()):
                case = table_shaft.item(j, 2).text()==table_point.item(i, 0).text()
                if case:
                    if angle >= 180: other = -1
                    else: other = 1
                    a = int(table_shaft.item(j, 1).text().replace("Point", ""))
                    x = sys.add_param(float(table_point.item(a, 1).text()))
                    y = sys.add_param(float(table_point.item(i, 2).text())*other)
                else:
                    x = sys.add_param(float(table_point.item(i, 1).text()))
                    y = sys.add_param(float(table_point.item(i, 2).text()))
            p = Point2d(Workplane1, x, y)
            Point += [p]
            if table_point.item(i, 3).checkState():
                Constraint.dragged(Workplane1, p)
        for i in range(table_chain.rowCount()):
            pa = int(table_chain.item(i, 1).text().replace("Point", ""))
            pb = int(table_chain.item(i, 2).text().replace("Point", ""))
            pc = int(table_chain.item(i, 3).text().replace("Point", ""))
            lenab = float(table_chain.item(i, 4).text())
            lenbc = float(table_chain.item(i, 5).text())
            lenac = float(table_chain.item(i, 6).text())
            Constraint.distance(lenab, Workplane1, Point[pa], Point[pb])
            Constraint.distance(lenbc, Workplane1, Point[pb], Point[pc])
            Constraint.distance(lenac, Workplane1, Point[pa], Point[pc])
        for i in range(table_line.rowCount()):
            start = int(table_line.item(i, 1).text().replace("Point", ""))
            end = int(table_line.item(i, 2).text().replace("Point", ""))
            len = float(table_line.item(i, 3).text())
            Constraint.distance(len, Workplane1, Point[start], Point[end])
        for i in range(table_slider.rowCount()):
            pt = int(table_slider.item(i, 1).text().replace("Point", ""))
            start = int(table_line.item(int(table_slider.item(i, 2).text().replace("Line", "")), 1).text().replace("Point", ""))
            end = int(table_line.item(int(table_slider.item(i, 2).text().replace("Line", "")), 2).text().replace("Point", ""))
            line = LineSegment2d(Workplane1, Point[start], Point[end])
            Constraint.on(Workplane1, Point[pt], line)
        for i in range(table_shaft.rowCount()):
            center = int(table_shaft.item(i, 1).text().replace("Point", ""))
            reference = int(table_shaft.item(i, 2).text().replace("Point", ""))
            line = LineSegment2d(Workplane1, Point[center], Point[reference])
            Constraint.angle(Workplane1, angle, line, Line0, False)
        #TODO: to be continue...
        sys.solve()
        x = 0
        y = 0
        if (sys.result == SLVS_RESULT_OKAY):
            x = sys.get_param((point_int+2)*2+5).val
            y = sys.get_param((point_int+2)*2+6).val
        elif (sys.result == SLVS_RESULT_INCONSISTENT): print ("SLVS_RESULT_INCONSISTENT")
        elif (sys.result == SLVS_RESULT_DIDNT_CONVERGE): print ("SLVS_RESULT_DIDNT_CONVERGE")
        elif (sys.result == SLVS_RESULT_TOO_MANY_UNKNOWNS): print ("SLVS_RESULT_TOO_MANY_UNKNOWNS")
        return x, y

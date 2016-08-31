# -*- coding: utf-8 -*-
from .slvs import *

def table_process(table_point, table_line, table_chain, table_shaft, table_slider, table_rod):
    sys = System(500)
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
    
    Point = [Point1]
    #Load tables to constraint
    for i in range(1, table_point.rowCount()):
        x = sys.add_param(float(table_point.item(i, 1).text()))
        y = sys.add_param(float(table_point.item(i, 2).text()))
        p = Point2d(Workplane1, x, y)
        Point += [p]
        if not(table_point.item(i, 3).checkState()==False):
            Constraint.dragged(Workplane1, p)
    for i in range(table_line.rowCount()):
        start = int(table_line.item(i, 1).text().replace("Point", ""))
        end = int(table_line.item(i, 2).text().replace("Point", ""))
        len = float(table_line.item(i, 3).text())
        Constraint.distance(len, Workplane1, Point[start], Point[end])
    for i in range(table_chain.rowCount()):
        pa = int(table_chain.item(i, 1).text().replace("Point", ""))
        pb = int(table_chain.item(i, 2).text().replace("Point", ""))
        pc = int(table_chain.item(i, 3).text().replace("Point", ""))
        lenab = float(table_chain.item(i, 4).text().replace("Point", ""))
        lenbc = float(table_chain.item(i, 5).text().replace("Point", ""))
        lenac = float(table_chain.item(i, 6).text().replace("Point", ""))
        Constraint.distance(lenab, Workplane1, Point[pa], Point[pb])
        Constraint.distance(lenbc, Workplane1, Point[pb], Point[pc])
        Constraint.distance(lenac, Workplane1, Point[pa], Point[pc])
    for i in range(table_shaft.rowCount()):
        start = int(table_shaft.item(i, 1).text().replace("Point", ""))
        end = int(table_shaft.item(i, 2).text().replace("Point", ""))
    pN = sys.add_param(10)
    pNN = sys.add_param(0.0)
    PointN = Point2d(Workplane1, pN, pNN)
    Point += [PointN]
    Constraint.dragged(Workplane1, Point[-1])
    Line0 = LineSegment2d(Workplane1, Point[1], Point[-1])
    for i in range(table_shaft.rowCount()):
        center = int(table_shaft.item(i, 1).text().replace("Point", ""))
        reference = int(table_shaft.item(i, 2).text().replace("Point", ""))
        angle = float(table_shaft.item(i, 3).text())
        line = LineSegment2d(Workplane1, Point[center], Point[reference])
        Constraint.angle(Workplane1, angle, line, Line0, False)
    #TODO: to be continue...
    
    sys.solve()
    result = []
    if (sys.result == SLVS_RESULT_OKAY):
        for i in range(table_point.rowCount()*2):
            result += [sys.get_param(i+7).val]
    elif (sys.result == SLVS_RESULT_INCONSISTENT): print ("SLVS_RESULT_INCONSISTENT")
    elif (sys.result == SLVS_RESULT_DIDNT_CONVERGE): print ("SLVS_RESULT_DIDNT_CONVERGE")
    elif (sys.result == SLVS_RESULT_TOO_MANY_UNKNOWNS): print ("SLVS_RESULT_TOO_MANY_UNKNOWNS")
    return result

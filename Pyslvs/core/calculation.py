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
    print("""
p7 = sys.add_param(0.0)
p8 = sys.add_param(0.0)
Point1 = Point2d(Workplane1, p7, p8)
Constraint.dragged(Workplane1, Point1)""")
    Point = [Point1]
    #Load tables to constraint
    for i in range(1, table_point.rowCount()):
        x = sys.add_param(int(float(table_point.item(i, 1).text())))
        y = sys.add_param(int(float(table_point.item(i, 2).text())))
        p = Point2d(Workplane1, x, y)
        Point += [p]
        print("p"+str(i+7)+" = sys.add_param("+str(float(table_point.item(i, 1).text()))+")")
        print("p"+str(i+8)+" = sys.add_param("+str(float(table_point.item(i, 2).text()))+")")
        print("Point"+str(i+1)+" = Point2d(Workplane1, p"+str(i+8)+", p"+str(i+9)+")")
        if not(table_point.item(i, 3).checkState()==False):
            Constraint.dragged(Workplane1, p)
            print("Constraint.dragged(Workplane1, Point"+str(i+1)+")")
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
        print("Constraint.distance("+str(lenab)+", Workplane1, Point"+str(pa+1)+", Point"+str(pb+1)+")")
        print("Constraint.distance("+str(lenbc)+", Workplane1, Point"+str(pb+1)+", Point"+str(pc+1)+")")
        print("Constraint.distance("+str(lenac)+", Workplane1, Point"+str(pa+1)+", Point"+str(pc+1)+")")
    for i in range(table_line.rowCount()):
        start = int(table_line.item(i, 1).text().replace("Point", ""))
        end = int(table_line.item(i, 2).text().replace("Point", ""))
        len = float(table_line.item(i, 3).text())
        Constraint.distance(len, Workplane1, Point[start], Point[end])
        print("Constraint.distance("+str(len)+", Workplane1, Point"+str(start+1)+", Point"+str(end+1)+")")
    for i in range(table_slider.rowCount()):
        pt = int(table_slider.item(i, 1).text().replace("Point", ""))
        start = int(table_line.item(int(table_slider.item(i, 2).text().replace("Line", "")), 1).text().replace("Point", ""))
        end = int(table_line.item(int(table_slider.item(i, 2).text().replace("Line", "")), 2).text().replace("Point", ""))
        line = LineSegment2d(Workplane1, Point[start], Point[end])
        Constraint.on(Workplane1, Point[pt], line)
        print("Constraint.on(Workplane1, Point"+str(pt+1)+", LineSegment2d(Workplane1, Point"+str(start+1)+", Point"+str(end+1)+")")
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

def path_process(start_angle, end_angle, point_list,
        table_point, table_line,
        table_chain, table_shaft,
        table_slider, table_rod):
    def Solve(point_int, angle, table_point, table_line, table_chain, table_shaft, table_slider, table_rod):
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
            for j in range(table_shaft.rowCount()):
                case = (table_shaft.item(j, 2).text()==table_point.item(i, 0).text()) and (angle >= 180)
                if case:
                    a = int(table_shaft.item(j, 1).text().replace("Point", ""))
                    other = -1
                    x = sys.add_param(int(float(table_point.item(a, 1).text())))
                else:
                    other = 1
                    x = sys.add_param(int(float(table_point.item(i, 1).text())))
            y = sys.add_param(float(table_point.item(i, 2).text())*other)
            p = Point2d(Workplane1, x, y)
            Point += [p]
            if table_point.item(i, 3).checkState()==True:
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
        pN = sys.add_param(10)
        pNN = sys.add_param(0.0)
        PointN = Point2d(Workplane1, pN, pNN)
        Point += [PointN]
        Constraint.dragged(Workplane1, Point[-1])
        Line0 = LineSegment2d(Workplane1, Point[0], Point[-1])
        for i in range(table_shaft.rowCount()):
            center = int(table_shaft.item(i, 1).text().replace("Point", ""))
            reference = int(table_shaft.item(i, 2).text().replace("Point", ""))
            line = LineSegment2d(Workplane1, Point[center], Point[reference])
            Constraint.angle(Workplane1, angle, line, Line0, False)
        #TODO: to be continue...
        sys.solve()
        x = None
        y = None
        if (sys.result == SLVS_RESULT_OKAY):
            x = sys.get_param((point_int+2)*2+3).val
            y = sys.get_param((point_int+2)*2+4).val
        elif (sys.result == SLVS_RESULT_INCONSISTENT): print ("SLVS_RESULT_INCONSISTENT")
        elif (sys.result == SLVS_RESULT_DIDNT_CONVERGE): print ("SLVS_RESULT_DIDNT_CONVERGE")
        elif (sys.result == SLVS_RESULT_TOO_MANY_UNKNOWNS): print ("SLVS_RESULT_TOO_MANY_UNKNOWNS")
        print(point_int, x, y, angle)
        return x, y
    
    Path = []
    for n in point_list:
        Xval = []
        Yval = []
        for i in range(int(start_angle), int(end_angle)+1, 5):
            x, y = Solve(n, i, table_point, table_line,
                table_chain, table_shaft, table_slider, table_rod)
            Xval += [x]
            Yval += [y]
        Path += [Xval, Yval]
    return Path

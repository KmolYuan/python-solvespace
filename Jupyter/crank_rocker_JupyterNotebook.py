from tmp.workplace.exposed.slvs import *
from math import *
from bokeh.plotting import figure, output_notebook, show

d0 = 90 #基線長度(mm)
n1 = 35 #短連桿長度(mm)
n2 = 70 #長連桿長度(mm)
t1 = 40 #三角形第一邊(mm)
t2 = 40 #三角形第二邊(mm)
t3 = 70 #三角形第三邊(mm)

#開始繪圖

def crank_rock(degree):
    sys = System(500)
    g = 1
    #原點Point0
    p0 = sys.add_param(0.0)
    p1 = sys.add_param(0.0)
    p2 = sys.add_param(0.0)
    Point0 = Point3d(p0, p1, p2)

    #XY法線
    qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
    p3 = sys.add_param(qw)
    p4 = sys.add_param(qx)
    p5 = sys.add_param(qy)
    p6 = sys.add_param(qz)
    Normal1 = Normal3d(p3, p4, p5, p6)

    #工作平面
    Workplane1 = Workplane(Point0, Normal1)

    #3D版的Point0=>Point1
    p7 = sys.add_param(0.0)
    p8 = sys.add_param(0.0)
    Point1 = Point2d(Workplane1, p7, p8)
    Constraint.dragged(Workplane1, Point1)

    #長連桿轉軸Point2，還有基線Line0。
    p9 = sys.add_param(d0)
    p10 = sys.add_param(0.0)
    Point2 = Point2d(Workplane1, p9, p10)
    Constraint.dragged(Workplane1, Point2)
    Line0 = LineSegment2d(Workplane1, Point1, Point2)

    #Angle約束判斷
    if degree >= 180:
        other = -1
    else:
        other = 1

    #三角形Point3 / Point4 / Point5
    p11 = sys.add_param(20.0)
    p12 = sys.add_param(20.0)
    Point3 = Point2d(Workplane1, p11, p12)
    p13 = sys.add_param(0.0)
    p14 = sys.add_param(10.0*other)
    Point4 = Point2d(Workplane1, p13, p14)
    p15 = sys.add_param(30.0)
    p16 = sys.add_param(20.0)
    Point5 = Point2d(Workplane1, p15, p16)
    Constraint.distance(t1, Workplane1, Point4, Point3)
    Constraint.distance(t2, Workplane1, Point3, Point5)
    Constraint.distance(t3, Workplane1, Point4, Point5)

    #連桿約束
    Constraint.distance(n1, Workplane1, Point1, Point4)
    Constraint.distance(n2, Workplane1, Point2, Point5)
    Line1 = LineSegment2d(Workplane1, Point1, Point4)

    #短連桿與水平軸的角度
    Constraint.angle(Workplane1, degree, Line1, Line0, False)

    #以下解題

    sys.solve()

    if (sys.result == SLVS_RESULT_OKAY):
        x = sys.get_param(11).val
        y = sys.get_param(12).val
        return x, y
    elif (sys.result == SLVS_RESULT_INCONSISTENT):
        print ("solve failed")
        print ("SLVS_RESULT_INCONSISTENT")
        print ("%d DOF" % sys.dof)
    elif (sys.result == SLVS_RESULT_DIDNT_CONVERGE):
        print ("solve failed")
        print ("SLVS_RESULT_DIDNT_CONVERGE")
        print ("%d DOF" % sys.dof)
    elif (sys.result == SLVS_RESULT_TOO_MANY_UNKNOWNS):
        print ("solve failed")
        print ("SLVS_RESULT_TOO_MANY_UNKNOWNS")
        print ("%d DOF" % sys.dof)

def crank_rock_M(degree):
    sys = System(500)
    g = 1
    #原點Point0
    p0 = sys.add_param(0.0)
    p1 = sys.add_param(0.0)
    p2 = sys.add_param(0.0)
    Point0 = Point3d(p0, p1, p2)

    #XY法線
    qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
    p3 = sys.add_param(qw)
    p4 = sys.add_param(qx)
    p5 = sys.add_param(qy)
    p6 = sys.add_param(qz)
    Normal1 = Normal3d(p3, p4, p5, p6)

    #工作平面
    Workplane1 = Workplane(Point0, Normal1)

    #3D版的Point0=>Point1
    p7 = sys.add_param(0.0)
    p8 = sys.add_param(0.0)
    Point1 = Point2d(Workplane1, p7, p8)
    Constraint.dragged(Workplane1, Point1)

    #長連桿轉軸Point2，還有基線Line0。
    p9 = sys.add_param(d0)
    p10 = sys.add_param(0.0)
    Point2 = Point2d(Workplane1, p9, p10)
    Constraint.dragged(Workplane1, Point2)
    Line0 = LineSegment2d(Workplane1, Point1, Point2)

    #Angle約束判斷
    if degree >= 180:
        other = -1
    else:
        other = 1

    #三角形Point3 / Point4 / Point5
    p11 = sys.add_param(20.0)
    p12 = sys.add_param(20.0)
    Point3 = Point2d(Workplane1, p11, p12)
    p13 = sys.add_param(0.0)
    p14 = sys.add_param(10.0*other)
    Point4 = Point2d(Workplane1, p13, p14)
    p15 = sys.add_param(30.0)
    p16 = sys.add_param(20.0)
    Point5 = Point2d(Workplane1, p15, p16)
    Constraint.distance(t1, Workplane1, Point4, Point3)
    Constraint.distance(t2, Workplane1, Point3, Point5)
    Constraint.distance(t3, Workplane1, Point4, Point5)

    #連桿約束
    Constraint.distance(n1, Workplane1, Point1, Point4)
    Constraint.distance(n2, Workplane1, Point2, Point5)
    Line1 = LineSegment2d(Workplane1, Point1, Point4)

    #短連桿與水平軸的角度
    Constraint.angle(Workplane1, degree, Line1, Line0, False)

    #以下解題

    sys.solve()

    if (sys.result == SLVS_RESULT_OKAY):
        x1 = sys.get_param(7).val
        y1 = sys.get_param(8).val
        x2 = sys.get_param(9).val
        y2 = sys.get_param(10).val
        x3 = sys.get_param(11).val
        y3 = sys.get_param(12).val
        x4 = sys.get_param(13).val
        y4 = sys.get_param(14).val
        x5 = sys.get_param(15).val
        y5 = sys.get_param(16).val
        return x1, y1, x2, y2, x3, y3, x4, y4, x5, y5
    elif (sys.result == SLVS_RESULT_INCONSISTENT):
        print ("solve failed")
        print ("SLVS_RESULT_INCONSISTENT")
        print ("%d DOF" % sys.dof)
    elif (sys.result == SLVS_RESULT_DIDNT_CONVERGE):
        print ("solve failed")
        print ("SLVS_RESULT_DIDNT_CONVERGE")
        print ("%d DOF" % sys.dof)
    elif (sys.result == SLVS_RESULT_TOO_MANY_UNKNOWNS):
        print ("solve failed")
        print ("SLVS_RESULT_TOO_MANY_UNKNOWNS")
        print ("%d DOF" % sys.dof)

#主程式
X1val  = []
Y1val  = []

for i in range(0, 361):
    x, y = crank_rock(i)
    X1val += [x]
    Y1val += [y]
x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = crank_rock_M(120)
X2val = [x1, x4, x3, x5, x4, x5, x2]
Y2val = [y1, y4, y3, y5, y4, y5, y2]
X3val = [x1, x2]
Y3val = [y1, y2]
print ("Solve Completed")

#bokeh
output_notebook()
plot = figure(title="simple line example", x_axis_label='x', y_axis_label='y')
plot.line(X1val, Y1val, legend="Mango.", line_width=2, line_color="blue")
plot.line(X2val, Y2val, legend="Mechanism.", line_width=4, line_color="red")
plot.line(X3val, Y3val, legend="Base Line.", line_width=3, line_dash=[4, 4], line_color="orange")
show(plot)
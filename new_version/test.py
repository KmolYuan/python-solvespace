#一三角形呆鍊，由一長一短的連桿固定在水平基線上。
#短連桿鎖固在原點上，長連桿鎖固在距原點90mm處。
#短連桿長度35mm；長連桿長度70mm。
#三角形呆鍊邊長分別為40mm、40mm、70mm
from slvs import *
from math import *

#相關參數
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
    Constraint.angle(Workplane1, degree, Line1, Line0)

    #以下解題

    result = sys.solve()

    if result == SLVS_RESULT_OKAY:
        print ("點座標：")
        print(("P3(%.3f %.3f %.3f)")%(sys.get_param(11).val, sys.get_param(12).val, sys.get_param(2).val))
        print(("P4(%.3f %.3f %.3f)")%(sys.get_param(13).val, sys.get_param(14).val, sys.get_param(2).val))
        print ("%d DOF" % sys.dof)
    elif result == SLVS_RESULT_INCONSISTENT:
        print ("solve failed")
        print ("SLVS_RESULT_INCONSISTENT")
        print ("%d DOF" % sys.dof)
    elif result == SLVS_RESULT_DIDNT_CONVERGE:
        print ("solve failed")
        print ("SLVS_RESULT_DIDNT_CONVERGE")
        print ("%d DOF" % sys.dof)
    elif result == SLVS_RESULT_TOO_MANY_UNKNOWNS:
        print ("solve failed")
        print ("SLVS_RESULT_TOO_MANY_UNKNOWNS")
        print ("%d DOF" % sys.dof)

#主程式
for i in range(0, 360, 10):
    print ("Degree: {:03} deg".format(i))
    crank_rock(i)
print ("Solve Completed")

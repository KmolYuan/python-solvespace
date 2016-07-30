#行程解題解題：兩個長1.5mm、2.3mm的連桿，在一直線上作動。
#原點的基座塊比工作路徑高0.5mm，寬0.75mm（占用0.38mm）。
#底線距離基座面3.25mm。
#2.3mm的連桿寬0.25mm，半圓頭。
#求最小行程（2.3mm的連桿與基座接觸）。
#求最大行程（半圓頭與底線接觸）。
from slvs import *
from math import *
sys = System(500)
g = 1

#相關參數
h0 = 0.5 #基塊高度(mm)
b0 = 0.75 #基塊寬度(mm)
n1 = 1.5 #後連桿長度(mm)
n2 = 2.3 #前連桿長度(mm)
R0 = 0.25 #半圓頭半徑(mm)
L0 = 3.25 #底線距離(mm)

#開始繪圖

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

#連桿中繼點Point2和行程點Point3
p9 = sys.add_param(2.0)
p10 = sys.add_param(2.0)
Point2 = Point2d(Workplane1, p9, p10)
p11 = sys.add_param(2.0)
p12 = sys.add_param(0.0)
Point3 = Point2d(Workplane1, p11, p12)
Line0 = LineSegment2d(Workplane1, Point1, Point3)
Constraint.horizontal(Workplane1, Line0)

#前連桿碰到基座
Line1 = LineSegment2d(Workplane1, Point2, Point3)
p13 = sys.add_param(b0/2)
p14 = sys.add_param(h0)
Point4 = Point2d(Workplane1, p13, p14)
Constraint.dragged(Workplane1, Point4) #必須鎖住已知點
Constraint.distance(R0, Workplane1, Point4, Line1)
Constraint.distance(n1, Workplane1, Point1, Point2)
Constraint.distance(n2, Workplane1, Point2, Point3)

#以下解題

sys.solve()

Ansmin = sys.get_param(11).val - b0/2
Ansmax = L0 - R0 - b0/2

if (sys.result == SLVS_RESULT_OKAY):
    print ("點座標：")
    print(("P1(%.3f %.3f %.3f)")%(sys.get_param(7).val, sys.get_param(8).val, sys.get_param(2).val))
    print("P1(0.000 0.000 0.000)")
    print(("P2(%.3f %.3f %.3f)")%(sys.get_param(9).val, sys.get_param(10).val, sys.get_param(2).val))
    print("P2(-0.400 1.450 0.000)")
    print(("P3(%.3f %.3f %.3f)")%(sys.get_param(11).val, sys.get_param(12).val, sys.get_param(2).val))
    print("P4(1.390 0.000 0.000)\n")
    print("Min:")
    print(("(%.3f)")%(Ansmin))
    print("Max:")
    print(("(%.3f)")%(Ansmax))
    print ("%d DOF" % sys.dof)
elif (sys.result == SLVS_RESULT_INCONSISTENT):
    print ("solve failed")
    print ("SLVS_RESULT_INCONSISTENT")
    print ("%d DOF" % sys.dof)
    for i in range(sys.faileds):
        print(" %lu", sys.failed[i]);
elif (sys.result == SLVS_RESULT_DIDNT_CONVERGE):
    print ("solve failed")
    print ("SLVS_RESULT_DIDNT_CONVERGE")
    print ("%d DOF" % sys.dof)
elif (sys.result == SLVS_RESULT_TOO_MANY_UNKNOWNS):
    print ("solve failed")
    print ("SLVS_RESULT_TOO_MANY_UNKNOWNS")
    print ("%d DOF" % sys.dof)
#鍊條解題：18齒與30齒的鏈條，上下外切線長為200。
#小圓圓心為原點，大圓圓心在X軸上，求四個切點的座標
from slvs import *
from math import *
sys = System(500)
g = 1

#相關參數
n0 = 20 #鍊條長度(mm)
n1 = 18 #小輪齒數(t)
n2 = 30 #大輪齒數(t)
#邊長為a的的正n邊形外接圓半徑為：
#R=a/(2*sin(pi/n)) or R=(a/2)*csc(pi/n)
R1 = n0/(2*sin(pi/n1))
R2 = n0/(2*sin(pi/n2))

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

#Point2
p9 = sys.add_param(0.0)
p10 = sys.add_param(200.0)
Point2 = Point2d(Workplane1, p9, p10)

#上端外切線的兩個點Point3和Point4
p11 = sys.add_param(0.0)
p12 = sys.add_param(500.0)
Point3 = Point2d(Workplane1, p11, p12)
p13 = sys.add_param(500.0)
p14 = sys.add_param(500.0)
Point4 = Point2d(Workplane1, p13, p14)

#下端外切線的兩個點Point5和Point6
p15 = sys.add_param(0.0)
p16 = sys.add_param(-500.0)
Point5 = Point2d(Workplane1, p15, p16)
p17 = sys.add_param(500.0)
p18 = sys.add_param(-500.0)
Point6 = Point2d(Workplane1, p17, p18)

#外切線
Line1 = LineSegment2d(Workplane1, Point3, Point4)
Line2 = LineSegment2d(Workplane1, Point5, Point6)

#圓弧
Arc1 = ArcOfCircle(Workplane1, Normal1, Point1, Point3, Point5)
Constraint.diameter(R1*2, Workplane1, Arc1)
Arc2 = ArcOfCircle(Workplane1, Normal1, Point2, Point6, Point4)
Constraint.diameter(R2*2, Workplane1, Arc2)

#X軸Line0
Line0 = LineSegment2d(Workplane1, Point1, Point2)
Constraint.horizontal(Workplane1, Line0)

#約束
Constraint.tangent(Arc1, Line1, False)
Constraint.tangent(Arc2, Line1, False)
Constraint.tangent(Arc2, Line2, True)
Constraint.distance(200.0, Workplane1, Point3, Point4)

#以下解題

sys.solve()

if (sys.result == SLVS_RESULT_OKAY):
    print ("兩點座標：")
    print(("(%.3f %.3f %.3f)")%(sys.get_param(7).val, sys.get_param(8).val, sys.get_param(2).val))
    print(("(%.3f %.3f %.3f)\n")%(sys.get_param(9).val, sys.get_param(10).val, sys.get_param(2).val))
    print ("上切點座標：")
    print(("(%.3f %.3f %.3f)")%(sys.get_param(11).val, sys.get_param(12).val, sys.get_param(2).val))
    print("(-10.770 56.570 0.000)")
    print(("(%.3f %.3f %.3f)")%(sys.get_param(13).val, sys.get_param(14).val, sys.get_param(2).val))
    print("(185.700 93.980 0.000)\n")
    print ("下切點座標：")
    print(("(%.3f %.3f %.3f)")%(sys.get_param(15).val, sys.get_param(16).val*(-1), sys.get_param(2).val))
    print("(-10.770 -56.570 0.000)")
    print(("(%.3f %.3f %.3f)")%(sys.get_param(17).val, sys.get_param(18).val*(-1), sys.get_param(2).val))
    print("(185.700 -93.980 0.000)\n")
    print ("導入函數測試：")
    print ("R1：")
    print(R1)
    print ("R2：")
    print(R2)
    print ("pi：")
    print(pi)
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
    for i in range(sys.faileds):
        print(" %lu", sys.failed[i]);
elif (sys.result == SLVS_RESULT_TOO_MANY_UNKNOWNS):
    print ("solve failed")
    print ("SLVS_RESULT_TOO_MANY_UNKNOWNS")
    print ("%d DOF" % sys.dof)
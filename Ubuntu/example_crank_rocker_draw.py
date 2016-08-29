#一三角形呆鍊，由一長一短的連桿固定在水平基線上。
#短連桿鎖固在原點上，長連桿鎖固在距原點90mm處。
#短連桿長度35mm；長連桿長度70mm。
#三角形呆鍊邊長分別為40mm、40mm、70mm
from slvs import *
from math import *
import matplotlib.pyplot as plt

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
    draw = []

    #原點Point0
    p0 = sys.add_param(0.0)
    p1 = sys.add_param(0.0)
    p2 = sys.add_param(0.0)
    draw += [Point3d(p0, p1, p2)]

    #XY法線
    qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
    p3 = sys.add_param(qw)
    p4 = sys.add_param(qx)
    p5 = sys.add_param(qy)
    p6 = sys.add_param(qz)
    Normal1 = Normal3d(p3, p4, p5, p6)

    #工作平面
    Workplane1 = Workplane(draw[0], Normal1)

    #3D版的Point0=>Point1
    p7 = sys.add_param(0.0)
    p8 = sys.add_param(0.0)
    draw += [Point2d(Workplane1, p7, p8)]
    Constraint.dragged(Workplane1, draw[1])

    #長連桿轉軸Point2，還有基線Line0。
    p9 = sys.add_param(d0)
    p10 = sys.add_param(0.0)
    draw += [Point2d(Workplane1, p9, p10)]
    Constraint.dragged(Workplane1, draw[2])
    Line0 = LineSegment2d(Workplane1, draw[1], draw[2])

    #Angle約束判斷
    if degree >= 180:
        other = -1
    else:
        other = 1

    #三角形Point3 / Point4 / Point5
    p11 = sys.add_param(20.0)
    p12 = sys.add_param(20.0)
    draw += [Point2d(Workplane1, p11, p12)]
    p13 = sys.add_param(0.0)
    p14 = sys.add_param(10.0*other)
    draw += [Point2d(Workplane1, p13, p14)]
    p15 = sys.add_param(30.0)
    p16 = sys.add_param(20.0)
    draw += [Point2d(Workplane1, p15, p16)]
    Constraint.distance(t1, Workplane1, draw[4], draw[3])
    Constraint.distance(t2, Workplane1, draw[3], draw[5])
    Constraint.distance(t3, Workplane1, draw[4], draw[5])

    #連桿約束
    Constraint.distance(n1, Workplane1, draw[1], draw[4])
    Constraint.distance(n2, Workplane1, draw[2], draw[5])
    Line1 = LineSegment2d(Workplane1, draw[1], draw[4])

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

#主程式
Xval  = []
Yval  = []

for i in range(0, 361, 5):
    x, y = crank_rock(i)
    Xval += [x]
    Yval += [y]
print ("Solve Completed")

plt.plot(Xval, Yval)
plt.ylabel('some numbers')
plt.show()
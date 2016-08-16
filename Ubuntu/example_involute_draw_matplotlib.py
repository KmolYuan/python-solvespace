#漸開線解題
#由端點Point3畫出圖形
from slvs import *
import matplotlib.pyplot as plt
from math import *

#參數
r = 10.0#基圓半徑

def Involute(degree):
    #角度換算：degree去除重複圈數
    d = r*(degree*pi/180)
    n = degree//360
    degree -= 360*n

    #開始繪圖
    sys = System(500)
    g = 1

    #3D原點Point0
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

    #2D原點Point1
    p7 = sys.add_param(0.0)
    p8 = sys.add_param(0.0)
    Point1 = Point2d(Workplane1, p7, p8)
    Constraint.dragged(Workplane1, Point1)

    #Angle約束判斷
    if degree >= 180:
        other = -1
    else:
        other = 1

    #Point2繞行圓周，距離r
    p9 = sys.add_param(0.0)
    p10 = sys.add_param(10.0*other)
    Point2 = Point2d(Workplane1, p9, p10)
    Constraint.distance(r, Workplane1, Point1, Point2)
    Line1 = LineSegment2d(Workplane1, Point1, Point2)

    #Point3距離Point2為目前圓周長
    #並且連線d會垂直半徑連線r
    p11 = sys.add_param(10.0*other)
    p12 = sys.add_param(10.0*other)
    Point3 = Point2d(Workplane1, p11, p12)
    if d == 0:
        Constraint.on(Workplane1, Point2, Point3)
    else:
        Line2 = LineSegment2d(Workplane1, Point2, Point3)
        Constraint.distance(d, Workplane1, Point2, Point3)
        Constraint.perpendicular(Workplane1, Line1, Line2, False)

    #輔助基線Line0
    p13 = sys.add_param(10.0)
    p14 = sys.add_param(0.0)
    Point4 = Point2d(Workplane1, p13, p14)
    Constraint.dragged(Workplane1, Point4)
    Line0 = LineSegment2d(Workplane1, Point1, Point4)

    #約束角度
    Constraint.angle(Workplane1, degree, Line1, Line0, False)

    #以下解題
    sys.solve()
    if (sys.result == SLVS_RESULT_OKAY):
        #回傳Point7
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
degree = 720
for i in range(0, degree+1, 1):
    x, y = Involute(i)
    Xval += [x]
    Yval += [y]
print ("Solve Completed")

plt.plot(Xval, Yval)
plt.xlabel('x coordinate')
plt.ylabel('y coordinate')
plt.title("Involute - "+str(degree)+" deg")
plt.show()
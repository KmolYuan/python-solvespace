#一三角形呆鍊，由一長一短的連桿固定在水平基線上。
#短連桿鎖固在原點上，長連桿鎖固在距原點90mm處。
#短連桿長度35mm；長連桿長度70mm。
#三角形呆鍊邊長分別為40mm、40mm、70mm
'''
example_crank_rocker_draw.py
python3 -m pip install matplotlib
Point1 (0, 0)
Point2(90, 0)
link1 length 35
link2 length 70
link3 length 70
triangle length 70, 40, 40
'''
from slvs import *
from math import *
import matplotlib.pyplot as plt

# variables
d0 = 90
n1 = 35
n2 = 70
t1 = 40
t2 = 40
t3 = 70

# use moving reference frame as p2 prime, increment angel is 5 degree
def crank_rocker(degree, p2x, p2y, p3x, p3y, p4x, p4y, p5x, p5y):
    sys = System()
    g = 1
    # origin Point zero
    p0 = sys.add_param(0.0)
    p1 = sys.add_param(0.0)
    p2 = sys.add_param(0.0)
    Point0 = Point3d(p0, p1, p2)

    # add normal vector
    qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
    p3 = sys.add_param(qw)
    p4 = sys.add_param(qx)
    p5 = sys.add_param(qy)
    p6 = sys.add_param(qz)
    Normal1 = Normal3d(p3, p4, p5, p6)

    # add workplane
    Workplane1 = Workplane(Point0, Normal1)

    # convert 3D point to 2D point
    p7 = sys.add_param(0.0)
    p8 = sys.add_param(0.0)
    Point1 = Point2d(Workplane1, p7, p8)
    Constraint.dragged(Workplane1, Point1)

    #add Point2 and Line0
    p9 = sys.add_param(d0)
    p10 = sys.add_param(0.0)
    Point2 = Point2d(Workplane1, p9, p10)
    Constraint.dragged(Workplane1, Point2)
    
    p11 = sys.add_param(p2x)
    p12 = sys.add_param(p2y)
    moving2 = Point2d(Workplane1, p11, p12)
    Constraint.dragged(Workplane1, moving2)
    # Line0 depends on Point1 and moving2
    Line0 = LineSegment2d(Workplane1, Point1, moving2)

    # triangle Point4- Point3-Point5
    p13 = sys.add_param(p3x)
    p14 = sys.add_param(p3y)
    Point3 = Point2d(Workplane1, p13, p14)
    p15 = sys.add_param(p4x)
    p16 = sys.add_param(p4y)
    Point4 = Point2d(Workplane1, p15, p16)
    p17 = sys.add_param(p5x)
    p18 = sys.add_param(p5y)
    Point5 = Point2d(Workplane1, p17, p18)
    Constraint.distance(t1, Workplane1, Point4, Point3)
    Constraint.distance(t2, Workplane1, Point3, Point5)
    Constraint.distance(t3, Workplane1, Point4, Point5)

    # add Line1 and link length constraints
    Constraint.distance(n1, Workplane1, Point1, Point4)
    Constraint.distance(n2, Workplane1, Point2, Point5)
    Line1 = LineSegment2d(Workplane1, Point1, Point4)

    #add rotation angle constraint
    Constraint.angle(Workplane1, degree, Line1, Line0, False)

    #solve for results
    sys.calculateFaileds = 1;

    sys.solve()
    result = sys.result

    if(result == SLVS_RESULT_OKAY):

        # return coordinates of Point3
        return sys.get_param(13).val, sys.get_param(14).val, sys.get_param(15).val, sys.get_param(16).val, sys.get_param(17).val, sys.get_param(18).val

    elif (result == SLVS_RESULT_INCONSISTENT):
        print ("solve failed", degree)
        print ("SLVS_RESULT_INCONSISTENT")
        print ("%d DOF" % sys.dof)
    elif (result == SLVS_RESULT_DIDNT_CONVERGE):
        print ("solve failed")
        print ("SLVS_RESULT_DIDNT_CONVERGE")
        print ("%d DOF" % sys.dof)
    elif (result == SLVS_RESULT_TOO_MANY_UNKNOWNS):
        print ("solve failed")
        print ("SLVS_RESULT_TOO_MANY_UNKNOWNS")
        print ("%d DOF" % sys.dof)

# main program
Xval  = []
Yval  = []
inc = 5
# initially Point3, Point4, Point5 coordinate
p3x = 20
p3y = 20
p4x = 0
p4y = 10
p5x = 30
p5y = 20
for i in range(0, 360+inc*3, inc):
    # moving reference point
    p2x = d0*cos(i*pi/180)
    p2y = d0*sin(i*pi/180)
    try:
        p3x, p3y, p4x, p4y, p5x, p5y = crank_rocker(inc, p2x, p2y, p3x, p3y, p4x, p4y, p5x, p5y)
        Xval += [p3x]
        Yval += [p3y]
        print(i, ":", round(p3x, 4), round(p3y, 4))
    except:
        pass
print ("Solve Completed")

plt.plot(Xval, Yval)
plt.xlabel('x coordinate')
plt.ylabel('y coordinate')
plt.show()

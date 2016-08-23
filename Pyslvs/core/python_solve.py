from .slvs import *
from .main import *

sysSet = 500

class Solve:
    def __init__(self):
        self.sys = System(sysSet)
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
        self.Workplane1 = Workplane(Point0, Normal1)
    
    def move_link(self, x1, y1, x2, y2, d, fixed):
        p7 = self.sys.add_param(x1)
        p8 = self.sys.add_param(y1)
        Point2 = Point2d(self.Workplane1, p7, p8)
        p9 = self.sys.add_param(x2)
        p10 = self.sys.add_param(y2)
        Point3 = Point2d(self.Workplane1, p9, p10)
        Constraint.distance(d, self.Workplane1, Point2, Point3)
        
        self.sys.solve()
        if (self.sys.result == SLVS_RESULT_OKAY):
            x1 = self.sys.get_param(7).val
            y1 = self.sys.get_param(8).val
            x2 = self.sys.get_param(10).val
            y2 = self.sys.get_param(11).val
        else:
            print("Error")

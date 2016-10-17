# -*- coding: utf-8 -*-
import sys, platform
py_nm = sys.version[0:sys.version.find(" ")][0:3]
load_test = False

if platform.system().lower()=="windows":
    if py_nm=="3.5":
        try:
            from pyslvs_library.py35w.slvs import *
            print("Successfully loaded.")
            load_test = True
        except ImportError: print("Failed. The Library has not been compiled!")
elif platform.system().lower()=="linux":
    if py_nm=="3.4":
        try:
            from pyslvs_library.py34.slvs import *
            print("Successfully loaded.")
            load_test = True
        except ImportError: print("Failed. The Library has not been compiled!")
    elif py_nm=="3.5":
        try:
            from pyslvs_library.py35.slvs import *
            print("Successfully loaded.")
            load_test = True
        except ImportError: print("Failed. The Library has not been compiled!")
else: print("Python Version Not Support.")

if load_test==True:
    try:
        # create a system with up to 20 parameters, entities and constraints
        # (If you use System(), you will get the default of 50 parameters, ...)
        sys = System(20)

        # A point, initially at (x y z) = (10 10 10)
        p1 = Point3d(Param(10.0), Param(10.0), Param(10.0), sys)
        # and a second point at (20 20 20)
        p2 = Point3d(Param(20.0), Param(20.0), Param(20.0), sys)
        # and a line segment connecting them.
        LineSegment3d(p1, p2)

        # The distance between the points should be 30.0 units.
        Constraint.distance(30.0, p1, p2)

        # Let's tell the solver to keep the second point as close to constant
        # as possible, instead moving the first point.
        sys.set_dragged(p2)

        # Now that we have written our system, we solve.
        sys.solve()

        if (sys.result == SLVS_RESULT_OKAY):
            print (("okay; now at (%.3f %.3f %.3f)\n" +
                "             (%.3f %.3f %.3f)")%(
                    sys.get_param(0).val, sys.get_param(1).val, sys.get_param(2).val,
                    sys.get_param(3).val, sys.get_param(4).val, sys.get_param(5).val))
            print ("%d DOF" % sys.dof)
        else:
            print ("solve failed")
    except: print("Test failed.")
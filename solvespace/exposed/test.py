#-----------------------------------------------------------------------------
# Some sample code for slvs.dll. We draw some geometric entities, provide
# initial guesses for their positions, and then constrain them. The solver
# calculates their new positions, in order to satisfy the constraints.
#
# Copyright 2008-2013 Jonathan Westhues.
# Ported to Python by Benjamin Koch
#-----------------------------------------------------------------------------

#from slvs import System, Param
from slvs import *
import unittest

verbose = False

def printf(fmt, *args):
    print (fmt % args)

class H(object):
    __slots__ = "handle"

    def __init__(self, h):
        self.handle = h

class TestSlvs(unittest.TestCase):
    def floatEqual(self, a, b):
        return abs(a-b) < 0.001

    def assertFloatEqual(self, a, b):
        if not isinstance(a, (int, long, float)) \
                or not isinstance(b, (int, long, float)):
            self.assertTrue(False, "not a float")
        if self.floatEqual(a, b):
            self.assertTrue(True)
        else:
            self.assertEqual(a, b)

    def assertFloatListEqual(self, xs, ys):
        if len(xs) != len(ys):
            self.assertListEqual(xs, ys)
        else:
            for i,a,b in zip(range(len(xs)), xs, ys):
                aL = isinstance(a, (list, tuple))
                bL = isinstance(b, (list, tuple))
                if aL and bL:
                    self.assertFloatListEqual(a, b)
                elif not self.floatEqual(a, b):
                    self.assertEqual(a, b, "in list at index %d" % i)
            self.assertTrue(True)

    def test_param(self):
        sys = System()

        p1 = Param(17.3)
        self.assertFloatEqual(p1.value, 17.3)

        p2 = Param(1.0)
        p3 = Param(0.0)
        e = sys.add_point3d(p1, p2, p3)

        self.assertFloatEqual(p1.value, 17.3)
        self.assertFloatEqual(p2.value,  1.0)
        self.assertFloatEqual(p3.value,  0.0)

        p1 = e.x()
        p2 = e.y()
        p3 = e.z()

        self.assertFloatEqual(p1.value, 17.3)
        self.assertFloatEqual(p2.value,  1.0)
        self.assertFloatEqual(p3.value,  0.0)

        self.assertEqual(p1.handle, 1)
        self.assertEqual(p2.handle, 2)
        self.assertEqual(p3.handle, 3)


        p4 = sys.add_param(42.7)
        self.assertFloatEqual(p4.value, 42.7)

    #-----------------------------------------------------------------------------
    # An example of a constraint in 3d. We create a single group, with some
    # entities and constraints.
    #-----------------------------------------------------------------------------
    def test_example3d(self):
        sys = System()

        # This will contain a single group, which will arbitrarily number 1.
        g = 1;

        # A point, initially at (x y z) = (10 10 10)
        a = sys.add_param(10.0)
        b = sys.add_param(10.0)
        c = sys.add_param(10.0)
        p1 = Point3d(a, b, c)
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
        Slvs_Solve(sys, g);

        if (sys.result == SLVS_RESULT_OKAY):
            if verbose:
                print (("okay; now at (%.3f %.3f %.3f)\n" +
                       "             (%.3f %.3f %.3f)") % (
                        sys.get_param(0).val, sys.get_param(1).val, sys.get_param(2).val,
                        sys.get_param(3).val, sys.get_param(4).val, sys.get_param(5).val))
                print ("%d DOF" % sys.dof)

            self.assertFloatEqual(sys.get_param(0).val,  2.698)
            self.assertFloatEqual(sys.get_param(1).val,  2.698)
            self.assertFloatEqual(sys.get_param(2).val,  2.698)
            self.assertFloatEqual(sys.get_param(3).val, 20.018)
            self.assertFloatEqual(sys.get_param(4).val, 20.018)
            self.assertFloatEqual(sys.get_param(5).val, 20.018)
            self.assertEqual(sys.dof, 5)
        else:
            self.assertTrue(False, "solve failed")

    #-----------------------------------------------------------------------------
    # An example of a constraint in 2d. In our first group, we create a workplane
    # along the reference frame's xy plane. In a second group, we create some
    # entities in that group and dimension them.
    #-----------------------------------------------------------------------------
    def test_example2d(self):
        sys = System()

        g = 1;
        # First, we create our workplane. Its origin corresponds to the origin
        # of our base frame (x y z) = (0 0 0)
        p1 = Point3d(Param(0.0), Param(0.0), Param(0.0), sys)
        # and it is parallel to the xy plane, so it has basis vectors (1 0 0)
        # and (0 1 0).
        #Slvs_MakeQuaternion(1, 0, 0,
        #                    0, 1, 0, &qw, &qx, &qy, &qz);
        qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0,
                                             0, 1, 0)
        wnormal = Normal3d(Param(qw), Param(qx), Param(qy), Param(qz), sys)

        wplane = Workplane(p1, wnormal)

        # Now create a second group. We'll solve group 2, while leaving group 1
        # constant; so the workplane that we've created will be locked down,
        # and the solver can't move it.
        g = 2
        sys.default_group = 2
        # These points are represented by their coordinates (u v) within the
        # workplane, so they need only two parameters each.
        p11 = sys.add_param(10.0)
        p301 = Point2d(wplane, p11, Param(20))
        self.assertEqual(p11.group, 2)
        self.assertEqual(p301.group, 2)
        self.assertEqual(p301.u().group, 2)
        self.assertEqual(p301.v().group, 2)

        p302 = Point2d(wplane, Param(20), Param(10))

        # And we create a line segment with those endpoints.
        line = LineSegment2d(wplane, p301, p302)
        

        # Now three more points.
        p303 = Point2d(wplane, Param(100), Param(120))

        p304 = Point2d(wplane, Param(120), Param(110))

        p305 = Point2d(wplane, Param(115), Param(115))

        # And arc, centered at point 303, starting at point 304, ending at
        # point 305.
        p401 = ArcOfCircle(wplane, wnormal, p303, p304, p305);

        # Now one more point, and a distance
        p306 = Point2d(wplane, Param(200), Param(200))

        p307 = Distance(wplane, Param(30.0))

        # And a complete circle, centered at point 306 with radius equal to
        # distance 307. The normal is 102, the same as our workplane.
        p402 = Circle(wplane, wnormal, p306, p307);


        # The length of our line segment is 30.0 units.
        Constraint.distance(30.0, wplane, p301, p302)

        # And the distance from our line segment to the origin is 10.0 units.
        Constraint.distance(10.0, wplane, p1, line)

        # And the line segment is vertical.
        Constraint.vertical(wplane, line)
        # And the distance from one endpoint to the origin is 15.0 units.
        Constraint.distance(15.0, wplane, p301, p1)

        if False:
            # And same for the other endpoint; so if you add this constraint then
            # the sketch is overconstrained and will signal an error.
            Constraint.distance(18.0, wplane, p302, p1)

        # The arc and the circle have equal radius.
        Constraint.equal_radius(wplane, p401, p402)
        # The arc has radius 17.0 units.
        Constraint.diameter(17.0*2, wplane, p401)

        # If the solver fails, then ask it to report which constraints caused
        # the problem.
        sys.calculateFaileds = 1;

        # And solve.
        result = sys.solve()

        if(result == SLVS_RESULT_OKAY):
            if verbose:
                printf("solved okay");
                printf("line from (%.3f %.3f) to (%.3f %.3f)",
                        sys.get_param(7).val, sys.get_param(8).val,
                        sys.get_param(9).val, sys.get_param(10).val);
            self.assertFloatEqual(sys.get_param( 7).val,  10.000)
            self.assertFloatEqual(sys.get_param( 8).val,  11.180)
            self.assertFloatEqual(sys.get_param( 9).val,  10.000)
            self.assertFloatEqual(sys.get_param(10).val, -18.820)

            if verbose:
                printf("arc center (%.3f %.3f) start (%.3f %.3f) finish (%.3f %.3f)",
                        sys.get_param(11).val, sys.get_param(12).val,
                        sys.get_param(13).val, sys.get_param(14).val,
                        sys.get_param(15).val, sys.get_param(16).val);
            self.assertFloatListEqual(
                map(lambda i: sys.get_param(i).val, range(11, 17)),
                [101.114, 119.042, 116.477, 111.762, 117.409, 114.197])

            if verbose:
                printf("circle center (%.3f %.3f) radius %.3f",
                        sys.get_param(17).val, sys.get_param(18).val,
                        sys.get_param(19).val);
                printf("%d DOF", sys.dof);
            self.assertFloatEqual(sys.get_param(17).val, 200.000)
            self.assertFloatEqual(sys.get_param(18).val, 200.000)
            self.assertFloatEqual(sys.get_param(19).val,  17.000)

            self.assertEqual(sys.dof, 6)
        else:
            if verbose:
                printf("solve failed: problematic constraints are:");
                for i in range(sys.faileds):
                    printf(" %lu", sys.failed[i]);
                printf("");
                if (sys.result == SLVS_RESULT_INCONSISTENT):
                    printf("system inconsistent");
                else:
                    printf("system nonconvergent");
            self.assertTrue(False, "solve failed")

    def test_with_solidpython(self):
        import solid

        sys = System()

        a = sys.add_param(10)
        b = sys.add_param(3)
        c = sys.add_param(17)
        d = sys.add_param(23)

        #NOTE We should use Point2d, but I don't want to
        #     create a workplane just for that.
        p1 = Point3d(Param(7), Param(2), Param(0), sys)

        poly = solid.polygon([[a,b],[c,d], [0,0], p1])

        self.assertEqual(
            solid.scad_render(poly),
            "\n\npolygon(paths = [[0, 1, 2, 3]], points = [[10.0000000000, 3.0000000000], [17.0000000000, 23.0000000000], [0, 0], [7.0000000000, 2.0000000000, 0.0000000000]]);")


    def test_to_openscad(self):
        sys = System()

        # We want to find the plane for three points. The points
        # shouldn't change, so we put them into another group.

        p1 = Point3d(1, 1, 9, sys)
        p2 = Point3d(5, 2, 2, sys)
        p3 = Point3d(0, 7, 5, sys)

        # Other entities go into another group
        sys.default_group = 2

        wrkpl = Workplane(p1, Normal3d(Param(1), Param(0), Param(0), Param(0), sys))

        # Some constraints: all points are in the plane
        # (p1 is its origin, so we don't need a constraint)
        Constraint.on(wrkpl, p2)
        Constraint.on(wrkpl, p3)

        # Solve it (group 2 is still active)
        sys.solve()

        self.assertEqual(sys.result, SLVS_RESULT_OKAY)
        self.assertFloatListEqual(wrkpl.origin().to_openscad(),
            [ 1.000, 1.000, 9.000 ])
        self.assertFloatListEqual(wrkpl.normal().vector(),
            [ 0.863, -0.261, 0.432, -0.000 ])
        self.assertFloatListEqual(wrkpl.to_openscad(),
            [[0.6270915888275256, -0.22570772255200192, 0.7455281102701327, 1.0], [-0.22570772255200203, 0.8633874310873447, 0.45124069832139596, 1.0], [-0.7455281102701327, -0.45124069832139607, 0.49047901991447185, 9.0], [0, 0, 0, 1]])

    def test_rendersystem_points_and_lines(self):
        from slvs_solid import RenderSystem, union, scad_render

        r = RenderSystem()
        r.itemscale = 4

        p1 = [ 2,  0, 0]
        p2 = [ 0,  0, 0]
        p3 = [ 2,  4, 2]
        p4 = [-3, 2, -2]

        pts = [ p1, p2, p3, p4 ]

        #obj = r.point3d([2, 0, 0]) + r.point3d([0, 0, 0]) + linear_extrude(height = 0.5)(polygon([[0,0,0], [2,0,0], [0,2,0]]))
        #obj = union()(map(r.point3d, pts)) + r.line3d(p3, p4)

        sys = System()
        p1s = Point3d(*(p1 + [sys]))
        p2s = Point3d(*(p2 + [sys]))
        p3s = Point3d(*(p3 + [sys]))
        p4s = Point3d(*(p4 + [sys]))
        line = LineSegment3d(p3s, p4s)

        obj = r.system(sys)

        self.assertEqual(scad_render(obj),
            '\n\nunion() {\n\tpolyhedron(points = [[2.0000000000, 0.0000000000, 0.0000000000], [1.8000000000, -0.1154800000, -0.3464000000], [2.2000000000, -0.1154800000, -0.3464000000], [2.0000000000, 0.2309200000, -0.3464000000], [1.8000000000, -0.1154800000, 0.3464000000], [2.2000000000, -0.1154800000, 0.3464000000], [2.0000000000, 0.2309200000, 0.3464000000]], triangles = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3], [0, 4, 5], [0, 4, 6], [0, 5, 6], [4, 5, 6]]);\n\tpolyhedron(points = [[0.0000000000, 0.0000000000, 0.0000000000], [-0.2000000000, -0.1154800000, -0.3464000000], [0.2000000000, -0.1154800000, -0.3464000000], [0.0000000000, 0.2309200000, -0.3464000000], [-0.2000000000, -0.1154800000, 0.3464000000], [0.2000000000, -0.1154800000, 0.3464000000], [0.0000000000, 0.2309200000, 0.3464000000]], triangles = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3], [0, 4, 5], [0, 4, 6], [0, 5, 6], [4, 5, 6]]);\n\tpolyhedron(points = [[2.0000000000, 4.0000000000, 2.0000000000], [1.8000000000, 3.8845200000, 1.6536000000], [2.2000000000, 3.8845200000, 1.6536000000], [2.0000000000, 4.2309200000, 1.6536000000], [1.8000000000, 3.8845200000, 2.3464000000], [2.2000000000, 3.8845200000, 2.3464000000], [2.0000000000, 4.2309200000, 2.3464000000]], triangles = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3], [0, 4, 5], [0, 4, 6], [0, 5, 6], [4, 5, 6]]);\n\tpolyhedron(points = [[-3.0000000000, 2.0000000000, -2.0000000000], [-3.2000000000, 1.8845200000, -2.3464000000], [-2.8000000000, 1.8845200000, -2.3464000000], [-3.0000000000, 2.2309200000, -2.3464000000], [-3.2000000000, 1.8845200000, -1.6536000000], [-2.8000000000, 1.8845200000, -1.6536000000], [-3.0000000000, 2.2309200000, -1.6536000000]], triangles = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3], [0, 4, 5], [0, 4, 6], [0, 5, 6], [4, 5, 6]]);\n\tmultmatrix(m = [[-0.7453559925, -0.4444444444, -0.2981423970, 2.0000000000], [-0.2981423970, -0.1777777778, 0.7453559925, 4.0000000000], [-0.5962847940, 0.6444444444, 0.0000000000, 2.0000000000], [0, 0, 0, 1]]) {\n\t\tlinear_extrude(height = 0.0400000000) {\n\t\t\tpolygon(paths = [[0, 1, 2, 3]], points = [[0, -0.0200000000], [0, 0.0200000000], [6.7082039325, 0.0200000000], [6.7082039325, -0.0200000000]]);\n\t\t}\n\t}\n}')


if __name__ == '__main__':
    unittest.main()

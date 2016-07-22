import math
from slvs  import *
from solid import *

sys = System()

# We want to find the plane for three points. The points
# shouldn't change, so we put them into another group.

p1 = Point3d(Param(1), Param(1), Param(9), sys)
p2 = Point3d(Param(5), Param(2), Param(2), sys)
p3 = Point3d(Param(0), Param(7), Param(5), sys)

#p1 = Point3d(Param(0), Param(0), Param(1), sys)
#p2 = Point3d(Param(5), Param(0), Param(1), sys)
#p3 = Point3d(Param(0), Param(7), Param(2), sys)

# Other entities go into another group
sys.default_group = 2

wrkpl = Workplane(p1, Normal3d(Param(1), Param(0), Param(0), Param(0), sys))

# Some constraints: all points are in the plane
# (p1 is its origin, so we don't need a constraint)
Constraint.on(wrkpl, p2)
Constraint.on(wrkpl, p3)

# Solve it (group 2 is still active)
sys.solve()

if(sys.result == SLVS_RESULT_OKAY):
    print "solved okay"
    for p in [p1, p2, p3]:
    	print "point at (%.3f, %.3f, %.3f)" % tuple(p.to_openscad())
    print "normal at (%.3f, %.3f, %.3f, %.3f)" % tuple(wrkpl.normal().vector())
    print wrkpl.to_openscad()
    print "%d DOF" % sys.dof
else:
    print("solve failed")


# draw some geometry, so we see the result

geom = union()

# a small triangle for each point
for p in [p1, p2, p3]:
	x = p.x().value
	y = p.y().value
	z = p.z().value

	w = 0.3

	geom.add(
		linear_extrude(height = z)(
			polygon([[x,y], [x-w,y], [x,y-w]])))

# draw plane: create flat surface in xy-plane and rotate+translate

plane = linear_extrude(height = 0.3)(
	square(size = [8, 8]))

# We call to_openscad to make sure it is called now, as
# we will change the points soon.
plane1 = multmatrix(wrkpl.to_openscad())(plane)

geom += plane1



# This time we do it without the solver.

# Move points, so the second plane won't overlap the first
p1.z().value += 2
p2.z().value += 2
p3.z().value += 2

plane2 = multmatrix(move_and_rotate(p1, p2, p3))(plane)
geom += plane2

scad_render_to_file(geom, "/tmp/out.scad")

from slvs_solid import *

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

print repr(scad_render(obj))
scad_render_to_file(obj, "/tmp/out.scad")

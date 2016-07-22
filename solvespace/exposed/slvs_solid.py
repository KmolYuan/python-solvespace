from slvs  import *
from solid import *


# call to_openscad(), if it exists
def _to_openscad(x):
    if hasattr(x, 'to_openscad'):
        return x.to_openscad()
    elif isinstance(x, list) or isinstance(x, tuple):
        return map(_to_openscad, x)
    else:
        return x

def mat_transpose(m):
    for i in range(4):
        for j in range(4):
            if i < j:
                a = m[i][j]
                b = m[j][i]
                m[i][j] = b
                m[j][i] = a


class RenderSystem(object):
    __slots__ = "itemscale"

    def __init__(self):
        self.itemscale = 1

    def point3d(self, pt, size = 0.1):
        pt = Vector(pt)
        size *= self.itemscale
        # We want equilateral triangles. I built that in
        # in SolveSpace and copied the dimensions.
        side = size
        hs = side/2
        height = size*0.8660
        center_to_baseline = size*0.2887
        center_to_top      = size*0.5773
        cb = center_to_baseline
        ct = center_to_top
        triangle = [ [-hs, -cb], [hs, -cb], [0, ct] ]
        pts = [ pt ]
        for z in [-height, +height]:
            for p in triangle:
                pts.append(pt + (p + [z]))
        ts = []
        for ps in [[0,1,2,3], [0,4,5,6]]:
            for a in range(0, 4):
                for b in range(a+1, 4):
                    for c in range(b+1, 4):
                        ts.append([ps[a], ps[b], ps[c]])
        return polyhedron(points = pts,
            #triangles = [[1,2,3],[4,6,5]])
            triangles = ts)

    def line3d(self, a, b, size = 0.01):
        a = Vector(a)
        b = Vector(b)
        length = (b-a).length()
        width = size*self.itemscale
        wh = width/2
        obj = linear_extrude(height = width)(
            polygon([ [0,-wh], [0, wh], [length, wh], [length, -wh] ]))
        return multmatrix(move_and_rotate(a, b, a+[0,0,1]))(obj)

    def system(self, system):
        obj = union()

        for i in range(system.entities):
            t = system.entity_type(i)
            if t == SLVS_E_POINT_IN_3D:
                obj.add(self.point3d(system.get_Point3d(i)))
            elif t == SLVS_E_LINE_SEGMENT:
                line = system.get_LineSegment3d(i)
                obj.add(self.line3d(line.a(), line.b()))

        return obj

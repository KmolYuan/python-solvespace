# -*- coding: utf-8 -*-
# cython: language_level=3

"""Wrapper source code of Solvespace.

author: Yuan Chang
copyright: Copyright (C) 2016-2019
license: AGPL
email: pyslvs@gmail.com
"""

from cpython.mem cimport PyMem_Malloc, PyMem_Free
from libcpp.vector cimport vector


cpdef tuple quaternion_u(double qw, double qx, double qy, double qz):
    cdef double x, y, z
    Slvs_QuaternionV(qw, qx, qy, qz, &x, &y, &z)
    return x, y, z


cpdef tuple quaternion_v(double qw, double qx, double qy, double qz):
    cdef double x, y, z
    Slvs_QuaternionV(qw, qx, qy, qz, &x, &y, &z)
    return x, y, z


cpdef tuple quaternion_n(double qw, double qx, double qy, double qz):
    cdef double x, y, z
    Slvs_QuaternionN(qw, qx, qy, qz, &x, &y, &z)
    return x, y, z


cpdef tuple make_quaternion(double ux, double uy, double uz, double vx, double vy, double vz):
    cdef double qw, qx, qy, qz
    Slvs_MakeQuaternion(ux, uy, uz, vx, vy, vz, &qw, &qx, &qy, &qz)
    return qw, qx, qy, qz


cdef inline list _get_params(list p_list, vector[Slvs_Param] &param, Params p):
    """Get the parameters after solved."""
    cdef size_t i
    for i in range(p.param_list.size()):
        p_list.append(param[<size_t>p.param_list[i]].val)
    return p_list


cdef class Params:

    """Python object to handle multiple parameter handles."""

    cdef vector[Slvs_hParam] param_list

    @staticmethod
    cdef Params create(Slvs_hParam *p, size_t count):
        """Constructor."""
        cdef Params params = Params.__new__(Params)
        cdef size_t i
        with nogil:
            for i in range(count):
                params.param_list.push_back(p[i])
        return params

    def __repr__(self) -> str:
        cdef str m = f"{self.__class__.__name__}(["
        cdef size_t i
        cdef size_t s = self.param_list.size()
        for i in range(s):
            m += str(<int>self.param_list[i])
            if i != s - 1:
                m += ", "
        m += "])"
        return m

# A virtual work plane that present 3D entity or constraint.
cdef Entity _WP_FREE_IN_3D = Entity.__new__(Entity)
_WP_FREE_IN_3D.t = SLVS_E_WORKPLANE
_WP_FREE_IN_3D.h = SLVS_FREE_IN_3D
_WP_FREE_IN_3D.g = 0
_WP_FREE_IN_3D.params = Params.create(NULL, 0)

# A "None" entity used to fill in constraint option.
cdef Entity _ENTITY_NONE = Entity.__new__(Entity)
_ENTITY_NONE.t = 0
_ENTITY_NONE.h = 0
_ENTITY_NONE.g = 0
_ENTITY_NONE.params = Params.create(NULL, 0)

# Entity names
cdef dict _ENTITY_NAME = {
    SLVS_E_POINT_IN_3D: "point 3d",
    SLVS_E_POINT_IN_2D: "point 2d",
    SLVS_E_NORMAL_IN_2D: "normal 2d",
    SLVS_E_NORMAL_IN_3D: "normal 3d",
    SLVS_E_DISTANCE: "distance",
    SLVS_E_WORKPLANE: "work plane",
    SLVS_E_LINE_SEGMENT: "line segment",
    SLVS_E_CUBIC: "cubic",
    SLVS_E_CIRCLE: "circle",
    SLVS_E_ARC_OF_CIRCLE: "arc",
}


cdef class Entity:

    """Python object to handle a pointer of 'Slvs_hEntity'."""

    cdef int t
    cdef Slvs_hEntity h, wp
    cdef Slvs_hGroup g
    cdef readonly Params params

    FREE_IN_3D = _WP_FREE_IN_3D
    NONE = _ENTITY_NONE

    @staticmethod
    cdef Entity create(Slvs_Entity *e, size_t p_size):
        """Constructor."""
        cdef Entity entity = Entity.__new__(Entity)
        with nogil:
            entity.t = e.type
            entity.h = e.h
            entity.wp = e.wrkpl
            entity.g = e.group
        entity.params = Params.create(e.param, p_size)
        return entity

    cdef inline bint is_3d(self):
        return self.wp == SLVS_FREE_IN_3D

    cdef inline bint is_none(self):
        return self.h == 0

    cdef inline bint is_point_2d(self):
        return self.t == SLVS_E_POINT_IN_2D

    cdef inline bint is_point_3d(self):
        return self.t == SLVS_E_POINT_IN_3D

    cdef inline bint is_point(self):
        return self.is_point_2d() or self.is_point_3d()

    cdef inline bint is_normal_2d(self):
        return self.t == SLVS_E_NORMAL_IN_2D

    cdef inline bint is_normal_3d(self):
        return self.t == SLVS_E_NORMAL_IN_3D

    cdef inline bint is_normal(self):
        return self.is_normal_2d() or self.is_normal_3d()

    cdef inline bint is_distance(self):
        return self.t == SLVS_E_DISTANCE

    cdef inline bint is_work_plane(self):
        return self.t == SLVS_E_WORKPLANE

    cdef inline bint is_line_2d(self):
        return self.is_line() and not self.is_3d()

    cdef inline bint is_line_3d(self):
        return self.is_line() and self.is_3d()

    cdef inline bint is_line(self):
        return self.t == SLVS_E_LINE_SEGMENT

    cdef inline bint is_cubic(self):
        return self.t == SLVS_E_CUBIC

    cdef inline bint is_circle(self):
        return self.t == SLVS_E_CIRCLE

    cdef inline bint is_arc(self):
        return self.t == SLVS_E_ARC_OF_CIRCLE

    def __repr__(self) -> str:
        cdef int h = <int>self.h
        cdef int g = <int>self.g
        cdef str t = _ENTITY_NAME[<int>self.t]
        return (
            f"{self.__class__.__name__}"
            f"(handle={h}, group={g}, type=<{t}>, is_3d={self.is_3d()}, params={self.params})"
        )


cdef class SolverSystem:

    """Python object of 'Slvs_System'."""

    cdef Slvs_hGroup g
    cdef Slvs_System sys
    cdef vector[Slvs_Param] param_list
    cdef vector[Slvs_Entity] entity_list
    cdef vector[Slvs_Constraint] cons_list
    cdef vector[Slvs_hConstraint] failed_list

    def __cinit__(self):
        self.g = 0
        self.sys.params = self.sys.entities = self.sys.constraints = 0

    cdef inline void copy_to_sys(self) nogil:
        """Copy data from stack into system."""
        # Copy
        cdef int i = 0
        cdef Slvs_Param param
        for param in self.param_list:
            self.sys.param[i] = param
            i += 1

        i = 0
        cdef Slvs_Entity entity
        for entity in self.entity_list:
            self.sys.entity[i] = entity
            i += 1

        i = 0
        cdef Slvs_Constraint con
        for con in self.cons_list:
            self.sys.constraint[i] = con
            i += 1

    cpdef void clear(self):
        self.param_list.clear()
        self.entity_list.clear()
        self.cons_list.clear()
        self.free()

    cdef inline void failed_collecting(self) nogil:
        """Collecting the failed constraints."""
        self.failed_list.clear()
        cdef int i
        for i in range(self.sys.faileds):
            self.failed_list.push_back(self.sys.failed[i])

    cdef inline void free(self):
        PyMem_Free(self.sys.param)
        PyMem_Free(self.sys.entity)
        PyMem_Free(self.sys.constraint)
        PyMem_Free(self.sys.failed)

    cpdef void set_group(self, size_t g):
        """Set the current group by integer."""
        self.g = <Slvs_hGroup>g

    cpdef int group(self):
        """Return the current group by integer."""
        return <int>self.g

    cpdef list params(self, Params p):
        """Get the parameters by Params object."""
        cdef list param_list = []
        _get_params(param_list, self.param_list, p)
        return param_list

    cpdef int dof(self):
        """Return the DOF of system."""
        return self.sys.dof

    cpdef list faileds(self):
        """Return the count of failed constraint."""
        return list(self.failed_list)

    cpdef int solve(self):
        """Solve the system."""
        # Parameters
        self.sys.param = <Slvs_Param *>PyMem_Malloc(self.param_list.size() * sizeof(Slvs_Param))

        # Entities
        self.sys.entity = <Slvs_Entity *>PyMem_Malloc(self.entity_list.size() * sizeof(Slvs_Entity))

        # Constraints
        cdef size_t cons_size = self.cons_list.size()
        self.sys.constraint = <Slvs_Constraint *>PyMem_Malloc(cons_size * sizeof(Slvs_Constraint))
        self.sys.failed = <Slvs_hConstraint *>PyMem_Malloc(cons_size * sizeof(Slvs_hConstraint))
        self.sys.faileds = cons_size

        # Copy to system
        self.copy_to_sys()
        # Solve
        Slvs_Solve(&self.sys, self.g)
        # Failed constraints and free memory.
        self.failed_collecting()
        self.free()
        return self.sys.result

    cpdef Entity create_2d_base(self):
        """Create a basic 2D system and return the work plane."""
        cdef double qw, qx, qy, qz
        qw, qx, qy, qz = make_quaternion(1, 0, 0, 0, 1, 0)
        cdef Entity origin = self.add_point_3d(0, 0, 0)
        cdef Entity nm = self.add_normal_3d(qw, qx, qy, qz)
        return self.add_work_plane(origin, nm)

    cdef inline Slvs_hParam new_param(self, double val) nogil:
        """Add a parameter."""
        self.sys.params += 1
        cdef Slvs_hParam h = <Slvs_hParam>self.sys.params
        self.param_list.push_back(Slvs_MakeParam(h, self.g, val))
        return h

    cdef inline Slvs_hEntity eh(self) nogil:
        """Return new entity handle."""
        self.sys.entities += 1
        return <Slvs_hEntity>self.sys.entities

    cpdef Entity add_point_2d(self, Entity wp, double u, double v):
        """Add 2D point."""
        if wp is None or not wp.is_work_plane():
            raise TypeError(f"{wp} is not a work plane")

        cdef Slvs_hParam u_p = self.new_param(u)
        cdef Slvs_hParam v_p = self.new_param(v)
        cdef Slvs_Entity e = Slvs_MakePoint2d(self.eh(), self.g, wp.h, u_p, v_p)
        self.entity_list.push_back(e)

        return Entity.create(&e, 2)

    cpdef Entity add_point_3d(self, double x, double y, double z):
        """Add 3D point."""
        cdef Slvs_hParam x_p = self.new_param(x)
        cdef Slvs_hParam y_p = self.new_param(y)
        cdef Slvs_hParam z_p = self.new_param(z)
        cdef Slvs_Entity e = Slvs_MakePoint3d(self.eh(), self.g, x_p, y_p, z_p)
        self.entity_list.push_back(e)

        return Entity.create(&e, 3)

    cpdef Entity add_normal_2d(self, Entity wp):
        """Add a 2D normal."""
        if wp is None or not wp.is_work_plane():
            raise TypeError(f"{wp} is not a work plane")

        cdef Slvs_Entity e = Slvs_MakeNormal2d(self.eh(), self.g, wp.h)
        self.entity_list.push_back(e)

        return Entity.create(&e, 0)

    cpdef Entity add_normal_3d(self, double qw, double qx, double qy, double qz):
        """Add a 3D normal."""
        cdef Slvs_hParam w_p = self.new_param(qw)
        cdef Slvs_hParam x_p = self.new_param(qx)
        cdef Slvs_hParam y_p = self.new_param(qy)
        cdef Slvs_hParam z_p = self.new_param(qz)
        cdef Slvs_Entity e = Slvs_MakeNormal3d(self.eh(), self.g, w_p, x_p, y_p, z_p)
        self.entity_list.push_back(e)

        return Entity.create(&e, 4)

    cpdef Entity add_distance(self, Entity wp, double d):
        """Add a 2D distance."""
        if wp is None or not wp.is_work_plane():
            raise TypeError(f"{wp} is not a work plane")

        cdef Slvs_hParam d_p = self.new_param(d)
        cdef Slvs_Entity e = Slvs_MakeDistance(self.eh(), self.g, wp.h, d_p)
        self.entity_list.push_back(e)

        return Entity.create(&e, 1)

    cpdef Entity add_line_2d(self, Entity wp, Entity p1, Entity p2):
        """Add a 2D line."""
        if wp is None or not wp.is_work_plane():
            raise TypeError(f"{wp} is not a work plane")
        if p1 is None or not p1.is_point_2d():
            raise TypeError(f"{p1} is not a 2d point")
        if p2 is None or not p2.is_point_2d():
            raise TypeError(f"{p2} is not a 2d point")

        cdef Slvs_Entity e = Slvs_MakeLineSegment(self.eh(), self.g, wp.h, p1.h, p2.h)
        self.entity_list.push_back(e)

        return Entity.create(&e, 0)

    cpdef Entity add_line_3d(self, Entity p1, Entity p2):
        """Add a 3D line."""
        if p1 is None or not p1.is_point_3d():
            raise TypeError(f"{p1} is not a 3d point")
        if p2 is None or not p2.is_point_3d():
            raise TypeError(f"{p2} is not a 3d point")

        cdef Slvs_Entity e = Slvs_MakeLineSegment(self.eh(), self.g, SLVS_FREE_IN_3D, p1.h, p2.h)
        self.entity_list.push_back(e)

        return Entity.create(&e, 0)

    cpdef Entity add_cubic(self, Entity wp, Entity p1, Entity p2, Entity p3, Entity p4):
        """Add a 2D cubic."""
        if wp is None or not wp.is_work_plane():
            raise TypeError(f"{wp} is not a work plane")
        if p1 is None or not p1.is_point_2d():
            raise TypeError(f"{p1} is not a 2d point")
        if p2 is None or not p2.is_point_2d():
            raise TypeError(f"{p2} is not a 2d point")
        if p3 is None or not p3.is_point_2d():
            raise TypeError(f"{p3} is not a 2d point")
        if p4 is None or not p4.is_point_2d():
            raise TypeError(f"{p4} is not a 2d point")

        cdef Slvs_Entity e = Slvs_MakeCubic(self.eh(), self.g, wp.h, p1.h, p2.h, p3.h, p4.h)
        self.entity_list.push_back(e)

        return Entity.create(&e, 0)

    cpdef Entity add_arc(self, Entity wp, Entity nm, Entity ct, Entity start, Entity end):
        """Add an 2D arc."""
        if wp is None or not wp.is_work_plane():
            raise TypeError(f"{wp} is not a work plane")
        if nm is None or not nm.is_normal_3d():
            raise TypeError(f"{nm} is not a 3d normal")
        if ct is None or not ct.is_point_2d():
            raise TypeError(f"{ct} is not a 2d point")
        if start is None or not start.is_point_2d():
            raise TypeError(f"{start} is not a 2d point")
        if end is None or not end.is_point_2d():
            raise TypeError(f"{end} is not a 2d point")

        cdef Slvs_Entity e = Slvs_MakeArcOfCircle(self.eh(), self.g, wp.h, nm.h, ct.h, start.h, end.h)
        self.entity_list.push_back(e)

        return Entity.create(&e, 0)

    cpdef Entity add_circle(self, Entity wp, Entity nm, Entity ct, Entity radius):
        """Add a 2D circle."""
        if wp is None or not wp.is_work_plane():
            raise TypeError(f"{wp} is not a work plane")
        if nm is None or not nm.is_normal_3d():
            raise TypeError(f"{nm} is not a 3d normal")
        if ct is None or not ct.is_point_2d():
            raise TypeError(f"{ct} is not a 2d point")
        if radius is None or not radius.is_distance():
            raise TypeError(f"{radius} is not a distance")

        cdef Slvs_Entity e = Slvs_MakeCircle(self.eh(), self.g, wp.h, ct.h, nm.h, radius.h)
        self.entity_list.push_back(e)

        return Entity.create(&e, 0)

    cpdef Entity add_work_plane(self, Entity origin, Entity nm):
        """Add a 3D work plane."""
        if origin is None or origin.t != SLVS_E_POINT_IN_3D:
            raise TypeError(f"{origin} is not a 3d point")
        if nm is None or nm.t != SLVS_E_NORMAL_IN_3D:
            raise TypeError(f"{nm} is not a 3d normal")

        cdef Slvs_Entity e = Slvs_MakeWorkplane(self.eh(), self.g, origin.h, nm.h)
        self.entity_list.push_back(e)

        return Entity.create(&e, 0)

    cpdef void add_constraint(
        self,
        Constraint c_type,
        Entity wp,
        double v,
        Entity p1,
        Entity p2,
        Entity e1,
        Entity e2,
        Entity e3,
        Entity e4,
        int other,
        int other2
    ):
        """Add customized constraint."""
        if wp is None or not wp.is_work_plane():
            raise TypeError(f"{wp} is not a work plane")

        cdef Entity e
        for e in (p1, p2):
            if e is None or not (e.is_none() or e.is_point()):
                raise TypeError(f"{e} is not a point")
        for e in (e1, e2, e3, e4):
            if e is None:
                raise TypeError(f"{e} is not a entity")

        self.sys.constraints += 1
        cdef Slvs_Constraint c
        c.h = <Slvs_hConstraint>self.sys.constraints
        c.group = self.g
        c.type = c_type
        c.wrkpl = wp.h
        c.valA = v
        c.ptA = p1.h
        c.ptB = p2.h
        c.entityA = e1.h
        c.entityB = e2.h
        c.entityC = e3.h
        c.entityD = e4.h
        c.other = other
        c.other2 = other2
        self.cons_list.push_back(c)

    #####
    # TODO: Constraint methods.
    #####

    cpdef void on(self):
        pass

    cpdef void distance(self):
        pass

    cpdef void equal(self):
        pass

    cpdef void ratio(self):
        pass

    cpdef void equal_point_to_line(self):
        pass

    cpdef void symmetric(self):
        pass

    cpdef void symmetric_h(self):
        pass

    cpdef void symmetric_v(self):
        pass

    cpdef void midpoint(self):
        pass

    cpdef void horizontal(self):
        pass

    cpdef void vertical(self):
        pass

    cpdef void diameter(self):
        pass

    cpdef void orientation(self):
        pass

    cpdef void angle(self):
        pass

    cpdef void perpendicular(self):
        pass

    cpdef void parallel(self):
        pass

    cpdef void tangent(self):
        pass

    cpdef void distance_proj(self):
        pass

    cpdef void dragged(self):
        pass

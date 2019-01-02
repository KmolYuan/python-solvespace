# -*- coding: utf-8 -*-
# cython: language_level=3

"""Wrapper source code of Solvespace.

author: Yuan Chang
copyright: Copyright (C) 2016-2019
license: AGPL
email: pyslvs@gmail.com
"""

from libc.stdlib cimport malloc, free
from libcpp.vector cimport vector

ctypedef Slvs_Param * Slvs_Param_ptr
ctypedef fused Plist:
    Slvs_Param_ptr
    vector[Slvs_Param]

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


cdef list _get_params(list p_list, Plist param, Params p):
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


cdef class Entity:

    """Python object to handle a pointer of 'Slvs_hEntity'."""

    cdef int t
    cdef Slvs_hEntity h
    cdef Slvs_hGroup g
    cdef readonly Params params

    @staticmethod
    cdef Entity create(Slvs_Entity *e, size_t p_size):
        """Constructor."""
        cdef Entity entity = Entity.__new__(Entity)
        entity.t = e.type
        entity.h = e.h
        entity.g = e.group
        entity.params = Params.create(e.param, p_size)
        return entity

    @staticmethod
    cdef Entity free_in_3d():
        """A virtual work plane that present 3D entity or constraint."""
        cdef Entity wp = Entity.__new__(Entity)
        wp.t = SLVS_E_WORKPLANE
        wp.h = SLVS_FREE_IN_3D
        wp.g = 0
        wp.params = Params.create(NULL, 0)
        return wp

    def __repr__(self) -> str:
        cdef int h = <int>self.h
        cdef int g = <int>self.g
        cdef int t = <int>self.t
        return (
            f"{self.__class__.__name__}"
            f"(handle={h}, group={g}, type={t}, params={self.params})"
        )


cdef class SolverSystem:

    """Python object of 'Slvs_System'."""

    cdef readonly bint solved
    cdef Slvs_hGroup g
    cdef Slvs_System sys
    cdef vector[Slvs_Param] param_list
    cdef vector[Slvs_Entity] entity_list
    cdef vector[Slvs_Constraint] cons_list

    def __cinit__(self):
        self.solved = False
        self.g = 0
        self.sys.params = self.sys.entities = self.sys.constraints = 0

    def __del__(self):
        free(self.sys.param)
        free(self.sys.entity)
        free(self.sys.constraint)
        free(self.sys.failed)

    cdef inline void copy_to_sys(self) nogil:
        """Copy data in to system."""
        # Copy
        cdef size_t i
        for i in range(self.param_list.size()):
            self.sys.param[i] = self.param_list[i]
        for i in range(self.entity_list.size()):
            self.sys.entity[i] = self.entity_list[i]
        for i in range(self.cons_list.size()):
            self.sys.constraint[i] = self.cons_list[i]

        # Clear all
        self.param_list.clear()
        self.entity_list.clear()
        self.cons_list.clear()

    cpdef void set_group(self, size_t g):
        """Set the current group by integer."""
        self.g = <Slvs_hGroup>g

    cpdef int group(self):
        """Return the current group by integer."""
        return <int>self.g

    cpdef double param(self, size_t p):
        """Return the value of the parameter."""
        if self.solved:
            return self.sys.param[p].val
        else:
            return self.param_list[p].val

    cdef list _params_unsolved(self, list p_list, Params p):
        """Get the parameters before solved."""
        cdef size_t i
        for i in range(p.param_list.size()):
            p_list.append(self.param_list[<size_t>p.param_list[i]].val)
        return p_list

    cdef list _params_solved(self, list p_list, Params p):
        """Get the parameters after solved."""
        cdef size_t i
        for i in range(p.param_list.size()):
            p_list.append(self.sys.param[<size_t>p.param_list[i]].val)
        return p_list

    cpdef list params(self, Params p):
        """Get the parameters by Params object."""
        cdef list param_list = []
        if self.solved:
            _get_params[Slvs_Param_ptr](param_list, self.sys.param, p)
        else:
            _get_params[vector[Slvs_Param]](param_list, self.param_list, p)
        return param_list

    cpdef int dof(self):
        """Return the DOF of system."""
        if self.solved:
            return self.sys.dof
        raise ValueError("the system has not been solved!")

    cpdef int solve(self):
        """Solve the system."""
        # Parameters
        self.sys.param = <Slvs_Param *>malloc(self.param_list.size() * sizeof(Slvs_Param))

        # Entities
        self.sys.entity = <Slvs_Entity *>malloc(self.entity_list.size() * sizeof(Slvs_Entity))

        # Constraints
        cdef size_t cons_size = self.cons_list.size()
        self.sys.constraint = <Slvs_Constraint *>malloc(cons_size * sizeof(Slvs_Constraint))
        self.sys.failed = <Slvs_hConstraint *>malloc(cons_size * sizeof(Slvs_hConstraint))
        self.sys.faileds = cons_size

        self.copy_to_sys()
        Slvs_Solve(&self.sys, self.g)
        self.solved = True

        return self.sys.result

    cdef inline Slvs_hParam new_param(self, double val) nogil:
        """Add a parameter."""
        cdef Slvs_hParam index = <Slvs_hParam>self.sys.params
        self.param_list.push_back(Slvs_MakeParam(index, self.g, val))
        self.sys.params += 1
        return index

    cdef inline void new_entity(self, Slvs_Entity entity) nogil:
        """Push back new entity."""
        self.entity_list.push_back(entity)
        self.sys.entities += 1

    cpdef Entity add_point_2d(self, Entity wp, double u, double v):
        """Add 2D point."""
        assert wp.t == SLVS_E_WORKPLANE, f"{wp} is not a work plane"

        cdef Slvs_hParam u_p = self.new_param(u)
        cdef Slvs_hParam v_p = self.new_param(v)
        cdef Slvs_hEntity i = <Slvs_hEntity>self.sys.entities
        cdef Slvs_Entity e = Slvs_MakePoint2d(i, self.g, wp.h, u_p, v_p)
        self.new_entity(e)

        return Entity.create(&e, 2)

    cpdef Entity add_point_3d(self, double x, double y, double z):
        """Add 3D point."""
        cdef Slvs_hParam x_p = self.new_param(x)
        cdef Slvs_hParam y_p = self.new_param(y)
        cdef Slvs_hParam z_p = self.new_param(z)
        cdef Slvs_hEntity i = <Slvs_hEntity>self.sys.entities
        cdef Slvs_Entity e = Slvs_MakePoint3d(i, self.g, x_p, y_p, z_p)
        self.new_entity(e)

        return Entity.create(&e, 3)

    cpdef Entity add_normal_3d(self, double qw, double qx, double qy, double qz):
        """Add a 3D normal."""
        cdef Slvs_hParam w_p = self.new_param(qw)
        cdef Slvs_hParam x_p = self.new_param(qx)
        cdef Slvs_hParam y_p = self.new_param(qy)
        cdef Slvs_hParam z_p = self.new_param(qz)
        cdef Slvs_hEntity i = <Slvs_hEntity>self.sys.entities
        cdef Slvs_Entity e = Slvs_MakeNormal3d(i, self.g, w_p, x_p, y_p, z_p)
        self.new_entity(e)

        return Entity.create(&e, 4)

    cpdef Entity add_normal_2d(self, Entity wp):
        """Add a 2D normal."""
        assert wp.t == SLVS_E_WORKPLANE, f"{wp} is not a work plane"

        cdef Slvs_hEntity i = <Slvs_hEntity>self.sys.entities
        cdef Slvs_Entity e = Slvs_MakeNormal2d(i, self.g, wp.h)
        self.new_entity(e)

        return Entity.create(&e, 0)

    cpdef Entity add_distance(self, Entity wp, double d):
        """Add a 2D distance."""
        assert wp.t == SLVS_E_WORKPLANE, f"{wp} is not a work plane"

        cdef Slvs_hParam d_p = self.new_param(d)
        cdef Slvs_hEntity i = <Slvs_hEntity>self.sys.entities
        cdef Slvs_Entity e = Slvs_MakeDistance(i, self.g, wp.h, d_p)
        self.new_entity(e)

        return Entity.create(&e, 1)

    cpdef Entity add_line_segment(self, Entity wp, Entity p1, Entity p2):
        """Add a 2D line segment."""
        assert wp.t == SLVS_E_WORKPLANE, f"{wp} is not a work plane"
        assert p1.t == SLVS_E_POINT_IN_2D, f"{p1} is not a 2d point"
        assert p2.t == SLVS_E_POINT_IN_2D, f"{p2} is not a 2d point"

        cdef Slvs_hEntity i = <Slvs_hEntity>self.sys.entities
        cdef Slvs_Entity e = Slvs_MakeLineSegment(i, self.g, wp.h, p1.h, p2.h)
        self.new_entity(e)

        return Entity.create(&e, 0)

    cpdef Entity add_cubic(self, Entity wp, Entity p1, Entity p2, Entity p3, Entity p4):
        """Add a 2D cubic."""
        assert wp.t == SLVS_E_WORKPLANE, f"{wp} is not a work plane"
        assert p1.t == SLVS_E_POINT_IN_2D, f"{p1} is not a 2d point"
        assert p2.t == SLVS_E_POINT_IN_2D, f"{p2} is not a 2d point"
        assert p3.t == SLVS_E_POINT_IN_2D, f"{p3} is not a 2d point"
        assert p4.t == SLVS_E_POINT_IN_2D, f"{p4} is not a 2d point"

        cdef Slvs_hEntity i = <Slvs_hEntity>self.sys.entities
        cdef Slvs_Entity e = Slvs_MakeCubic(i, self.g, wp.h, p1.h, p2.h, p3.h, p4.h)
        self.new_entity(e)

        return Entity.create(&e, 0)

    cpdef Entity add_arc(self, Entity wp, Entity nm, Entity ct, Entity start, Entity end):
        """Add an 2D arc."""
        assert wp.t == SLVS_E_WORKPLANE, f"{wp} is not a work plane"
        assert nm.t == SLVS_E_NORMAL_IN_3D, f"{nm} is not a 3d normal"
        assert ct.t == SLVS_E_POINT_IN_2D, f"{ct} is not a 2d point"
        assert start.t == SLVS_E_POINT_IN_2D, f"{start} is not a 2d point"
        assert end.t == SLVS_E_POINT_IN_2D, f"{end} is not a 2d point"

        cdef Slvs_hEntity i = <Slvs_hEntity>self.sys.entities
        cdef Slvs_Entity e = Slvs_MakeArcOfCircle(i, self.g, wp.h, nm.h, ct.h, start.h, end.h)
        self.new_entity(e)

        return Entity.create(&e, 0)

    cpdef Entity add_circle(self, Entity wp, Entity ct, Entity nm, Entity radius):
        """Add a 2D circle."""
        assert wp.t == SLVS_E_WORKPLANE, f"{wp} is not a work plane"
        assert ct.t == SLVS_E_POINT_IN_2D, f"{ct} is not a 2d point"
        assert nm.t == SLVS_E_NORMAL_IN_3D, f"{nm} is not a 3d normal"
        assert radius.t == SLVS_E_DISTANCE, f"{radius} is not a distance"

        cdef Slvs_hEntity i = <Slvs_hEntity>self.sys.entities
        cdef Slvs_Entity e = Slvs_MakeCircle(i, self.g, wp.h, ct.h, nm.h, radius.h)
        self.new_entity(e)

        return Entity.create(&e, 0)

    cpdef Entity add_work_plane(self, Entity origin, Entity nm):
        """Add a 3D work plane."""
        assert origin.t == SLVS_E_POINT_IN_3D, f"{origin} is not a 3d point"
        assert nm.t == SLVS_E_NORMAL_IN_3D, f"{nm} is not a 3d normal"

        cdef Slvs_hEntity i = <Slvs_hEntity>self.sys.entities
        cdef Slvs_Entity e = Slvs_MakeWorkplane(i, self.g, origin.h, nm.h)
        self.new_entity(e)

        return Entity.create(&e, 0)

    cpdef Entity create_2d_base(self):
        """Create a basic 2D system and return the work plane."""
        cdef double qw, qx, qy, qz
        qw, qx, qy, qz = make_quaternion(1, 0, 0, 0, 1, 0)
        cdef Entity origin = self.add_point_3d(0, 0, 0)
        cdef Entity nm = self.add_normal_3d(qw, qx, qy, qz)
        return self.add_work_plane(origin, nm)

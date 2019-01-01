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
    cdef Entity create(Slvs_Entity *e, size_t params):
        """Constructor."""
        cdef Entity entity = Entity.__new__(Entity)
        entity.t = e.type
        entity.h = e.h
        entity.g = e.group
        entity.params = Params.create(e.param, params)
        return entity

    def __repr__(self) -> str:
        cdef int h = <int>self.h
        cdef int g = <int>self.g
        cdef int t = <int>self.t
        return (
            f"{self.__class__.__name__}"
            f"(handle={h}, group={g}, type={t}, params={self.params})"
        )


cdef list _get_params(list p_list, Plist param, Params p):
    """Get the parameters after solved."""
    cdef size_t i
    for i in range(p.param_list.size()):
        p_list.append(param[<size_t>p.param_list[i]].val)
    return p_list


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

    # TODO: More methods.

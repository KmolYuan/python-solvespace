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


cdef class Entity:

    """Python object to handle a pointer of 'Slvs_hEntity'."""

    cdef Slvs_hEntity h
    cdef Slvs_hGroup g
    cdef int t

    @staticmethod
    cdef Entity create(Slvs_Entity *e):
        cdef Entity entity = Entity.__new__(Entity)
        entity.h = e.h
        entity.g = e.group
        entity.t = e.type
        return entity

    def __repr__(self) -> str:
        cdef int h = <int>self.h
        cdef int g = <int>self.g
        cdef int t = <int>self.t
        return f"Entity({h}, {g}, {t})"


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
        cdef Slvs_Entity e = Slvs_MakePoint2d(<Slvs_hEntity>self.sys.params, self.g, wp.h, u_p, v_p)
        self.new_entity(e)

        return Entity.create(&e)

    # TODO: More methods.

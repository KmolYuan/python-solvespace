# -*- coding: utf-8 -*-
# cython: language_level=3

"""Wrapper header of Solvespace.

author: Yuan Chang
copyright: Copyright (C) 2016-2019
license: AGPL
email: pyslvs@gmail.com
"""

from libc.stdint cimport uint32_t

cdef extern from "slvs.h" nogil:

    ctypedef uint32_t Slvs_hParam
    ctypedef uint32_t Slvs_hEntity
    ctypedef uint32_t Slvs_hConstraint
    ctypedef uint32_t Slvs_hGroup

    # Virtual work plane entity
    Slvs_hEntity SLVS_FREE_IN_3D

    ctypedef struct Slvs_Param:
        Slvs_hParam h
        Slvs_hGroup group
        double val

    # Entity type
    int SLVS_E_POINT_IN_3D
    int SLVS_E_POINT_IN_2D

    int SLVS_E_NORMAL_IN_2D
    int SLVS_E_NORMAL_IN_3D

    int SLVS_E_DISTANCE

    int SLVS_E_WORKPLANE
    int SLVS_E_LINE_SEGMENT
    int SLVS_E_CUBIC
    int SLVS_E_CIRCLE
    int SLVS_E_ARC_OF_CIRCLE

    ctypedef struct Slvs_Entity:
        Slvs_hEntity h
        Slvs_hGroup group
        int type
        Slvs_hEntity wrkpl
        Slvs_hEntity point[4]
        Slvs_hEntity normal
        Slvs_hEntity distance
        Slvs_hParam param[4]

    ctypedef struct Slvs_Constraint:
        Slvs_hConstraint h
        Slvs_hGroup group
        int type
        Slvs_hEntity wrkpl
        double valA
        Slvs_hEntity ptA
        Slvs_hEntity ptB
        Slvs_hEntity entityA
        Slvs_hEntity entityB
        Slvs_hEntity entityC
        Slvs_hEntity entityD
        int other
        int other2

    ctypedef struct Slvs_System:
        Slvs_Param *param
        int params
        Slvs_Entity *entity
        int entities
        Slvs_Constraint *constraint
        int constraints
        Slvs_hParam dragged[4]
        int calculateFaileds
        Slvs_hConstraint *failed
        int faileds
        int dof
        int result

    void Slvs_Solve(Slvs_System *sys, Slvs_hGroup hg)
    void Slvs_QuaternionU(
        double qw, double qx, double qy, double qz,
        double *x, double *y, double *z
    )
    void Slvs_QuaternionV(
        double qw, double qx, double qy, double qz,
        double *x, double *y, double *z
    )
    void Slvs_QuaternionN(
        double qw, double qx, double qy, double qz,
        double *x, double *y, double *z
    )
    void Slvs_MakeQuaternion(
        double ux, double uy, double uz,
        double vx, double vy, double vz,
        double *qw, double *qx, double *qy, double *qz
    )
    Slvs_Param Slvs_MakeParam(Slvs_hParam h, Slvs_hGroup group, double val)
    Slvs_Entity Slvs_MakePoint2d(
        Slvs_hEntity h, Slvs_hGroup group,
        Slvs_hEntity wrkpl,
        Slvs_hParam u, Slvs_hParam v
    )
    Slvs_Entity Slvs_MakePoint3d(
        Slvs_hEntity h, Slvs_hGroup group,
        Slvs_hParam x, Slvs_hParam y, Slvs_hParam z
    )
    Slvs_Entity Slvs_MakeNormal3d(
        Slvs_hEntity h, Slvs_hGroup group,
        Slvs_hParam qw, Slvs_hParam qx,
        Slvs_hParam qy, Slvs_hParam qz
    )
    Slvs_Entity Slvs_MakeNormal2d(
        Slvs_hEntity h, Slvs_hGroup group,
        Slvs_hEntity wrkpl
    )
    Slvs_Entity Slvs_MakeDistance(
        Slvs_hEntity h, Slvs_hGroup group,
        Slvs_hEntity wrkpl, Slvs_hParam d
    )
    Slvs_Entity Slvs_MakeLineSegment(
        Slvs_hEntity h, Slvs_hGroup group,
        Slvs_hEntity wrkpl,
        Slvs_hEntity ptA, Slvs_hEntity ptB
    )
    Slvs_Entity Slvs_MakeCubic(
        Slvs_hEntity h, Slvs_hGroup group,
        Slvs_hEntity wrkpl,
        Slvs_hEntity pt0, Slvs_hEntity pt1,
        Slvs_hEntity pt2, Slvs_hEntity pt3
    )
    Slvs_Entity Slvs_MakeArcOfCircle(
        Slvs_hEntity h, Slvs_hGroup group,
        Slvs_hEntity wrkpl,
        Slvs_hEntity normal,
        Slvs_hEntity center,
        Slvs_hEntity start, Slvs_hEntity end
    )
    Slvs_Entity Slvs_MakeCircle(
        Slvs_hEntity h, Slvs_hGroup group,
        Slvs_hEntity wrkpl,
        Slvs_hEntity center,
        Slvs_hEntity normal, Slvs_hEntity radius
    )
    Slvs_Entity Slvs_MakeWorkplane(
        Slvs_hEntity h, Slvs_hGroup group,
        Slvs_hEntity origin, Slvs_hEntity normal
    )
    Slvs_Constraint Slvs_MakeConstraint(
        Slvs_hConstraint h,
        Slvs_hGroup group,
        int type,
        Slvs_hEntity wrkpl,
        double valA,
        Slvs_hEntity ptA,
        Slvs_hEntity ptB,
        Slvs_hEntity entityA,
        Slvs_hEntity entityB
    )


cpdef enum Constraint:
    # Expose macro of constrain types
    POINTS_COINCIDENT = 100000
    PT_PT_DISTANCE
    PT_PLANE_DISTANCE
    PT_LINE_DISTANCE
    PT_FACE_DISTANCE
    PT_IN_PLANE
    PT_ON_LINE
    PT_ON_FACE
    EQUAL_LENGTH_LINES
    LENGTH_RATIO
    EQ_LEN_PT_LINE_D
    EQ_PT_LN_DISTANCES
    EQUAL_ANGLE
    EQUAL_LINE_ARC_LEN
    SYMMETRIC
    SYMMETRIC_HORIZ
    SYMMETRIC_VERT
    SYMMETRIC_LINE
    AT_MIDPOINT
    HORIZONTAL
    VERTICAL
    DIAMETER
    PT_ON_CIRCLE
    SAME_ORIENTATION
    ANGLE
    PARALLEL
    PERPENDICULAR
    ARC_LINE_TANGENT
    CUBIC_LINE_TANGENT
    EQUAL_RADIUS
    PROJ_PT_DISTANCE
    WHERE_DRAGGED
    CURVE_CURVE_TANGENT
    LENGTH_DIFFERENCE


cpdef enum ResultFlag:
    # Expose macro of result flags
    OKAY
    INCONSISTENT
    DIDNT_CONVERGE
    TOO_MANY_UNKNOWNS

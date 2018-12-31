# -*- coding: utf-8 -*-
# cython: language_level=3

"""Wrapper header of Solvespace.

author: Yuan Chang
copyright: Copyright (C) 2016-2018
license: AGPL
email: pyslvs@gmail.com
"""

from libc.stdint cimport uint32_t

cdef extern from "slvs.h" nogil:

    ctypedef uint32_t Slvs_hParam
    ctypedef uint32_t Slvs_hEntity
    ctypedef uint32_t Slvs_hConstraint
    ctypedef uint32_t Slvs_hGroup

    int SLVS_FREE_IN_3D

    ctypedef struct Slvs_Param:
        Slvs_hParam h
        Slvs_hGroup group
        double val

    int SLVS_E_POINT_IN_3D
    int SLVS_E_POINT_IN_2D

    int SLVS_E_NORMAL_IN_3D
    int SLVS_E_NORMAL_IN_2D

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

    int SLVS_C_POINTS_COINCIDENT
    int SLVS_C_PT_PT_DISTANCE
    int SLVS_C_PT_PLANE_DISTANCE
    int SLVS_C_PT_LINE_DISTANCE
    int SLVS_C_PT_FACE_DISTANCE
    int SLVS_C_PT_IN_PLANE
    int SLVS_C_PT_ON_LINE
    int SLVS_C_PT_ON_FACE
    int SLVS_C_EQUAL_LENGTH_LINES
    int SLVS_C_LENGTH_RATIO
    int SLVS_C_EQ_LEN_PT_LINE_D
    int SLVS_C_EQ_PT_LN_DISTANCES
    int SLVS_C_EQUAL_ANGLE
    int SLVS_C_EQUAL_LINE_ARC_LEN
    int SLVS_C_SYMMETRIC
    int SLVS_C_SYMMETRIC_HORIZ
    int SLVS_C_SYMMETRIC_VERT
    int SLVS_C_SYMMETRIC_LINE
    int SLVS_C_AT_MIDPOINT
    int SLVS_C_HORIZONTAL
    int SLVS_C_VERTICAL
    int SLVS_C_DIAMETER
    int SLVS_C_PT_ON_CIRCLE
    int SLVS_C_SAME_ORIENTATION
    int SLVS_C_ANGLE
    int SLVS_C_PARALLEL
    int SLVS_C_PERPENDICULAR
    int SLVS_C_ARC_LINE_TANGENT
    int SLVS_C_CUBIC_LINE_TANGENT
    int SLVS_C_EQUAL_RADIUS
    int SLVS_C_PROJ_PT_DISTANCE
    int SLVS_C_WHERE_DRAGGED
    int SLVS_C_CURVE_CURVE_TANGENT
    int SLVS_C_LENGTH_DIFFERENCE

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

    int SLVS_RESULT_OKAY
    int SLVS_RESULT_INCONSISTENT
    int SLVS_RESULT_DIDNT_CONVERGE
    int SLVS_RESULT_TOO_MANY_UNKNOWNS

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

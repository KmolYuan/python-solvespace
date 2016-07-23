#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension


slvs_module = Extension('_slvs',
                            sources=['../win32/w32util.cpp',
                            '../entity.cpp',
                            '../expr.cpp',
                            '../constrainteq.cpp',
                            '../system.cpp',
                            'lib.cpp'],
                           )

setup (name = 'slvs',
       version = '0.1',
       author      = "SWIG Docs",
       description = """Simple swig example from docs""",
       ext_modules = [slvs_module],
       py_modules = ["slvs"],
       )
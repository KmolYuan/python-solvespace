# -*- coding: utf-8 -*-

"""Compile the Cython libraries of Pyslvs."""

from distutils.core import setup, Extension
from platform import system
from Cython.Distutils import build_ext
from distutils import sysconfig

ver = sysconfig.get_config_var('VERSION')
lib = sysconfig.get_config_var('BINDIR')


macros = [
    ('_hypot', 'hypot'),
    ('ISOLATION_AWARE_ENABLED', None),
    ('LIBRARY', None),
    ('DLL_EXPORT', None),
    # ('_DEBUG', None),
    ('_CRT_SECURE_NO_WARNINGS', None),
]

compile_args = [
    '-O3',
    '-Wno-cpp',
    '-g',
    '-Wno-write-strings',
    '-fpermissive',
    '-fPIC',
    # '-std=c++11',
]

sources = [
    'src/' + 'slvs.pyx',
    'src/' + 'util.cpp',
    'src/' + 'entity.cpp',
    'src/' + 'expr.cpp',
    'src/' + 'constrainteq.cpp',
    'src/' + 'constraint.cpp',
    'src/' + 'system.cpp',
    'src/' + 'lib.cpp',
]

if system() == 'Windows':
    # Avoid compile error with CYTHON_USE_PYLONG_INTERNALS.
    # https://github.com/cython/cython/issues/2670#issuecomment-432212671
    macros.append(('MS_WIN64', None))
    # Disable format warning.
    compile_args.append('-Wno-format')

    # Solvespace arguments.
    macros.append(('WIN32', None))
    # macros.append(('_USE_MATH_DEFINES', None))

    # Platform sources.
    sources.append('src/platform/' + 'w32util.cpp')
    sources.append('src/platform/' + 'platform.cpp')
else:
    sources.append('src/platform/' + 'unixutil.cpp')

setup(ext_modules=[Extension(
    "slvs",
    sources=sources,
    language="c++",
    include_dirs=['include', 'src', 'src/platform'],
    define_macros=macros,
    extra_compile_args=compile_args,
)], cmdclass={'build_ext': build_ext})

# -*- coding: utf-8 -*-

"""Compile the Cython libraries of Python-Solvespace."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from setuptools import setup, Extension, find_packages
from platform import system
from distutils import sysconfig

src_path = 'src/'
platform_path = src_path + 'platform/'
ver = sysconfig.get_config_var('VERSION')
lib = sysconfig.get_config_var('BINDIR')

with open("README.md", "r") as f:
    long_description = f.read()

macros = [
    ('_hypot', 'hypot'),
    ('M_PI', 'PI'),  # C++ 11
    ('ISOLATION_AWARE_ENABLED', None),
    ('LIBRARY', None),
    ('EXPORT_DLL', None),
    ('_CRT_SECURE_NO_WARNINGS', None),
]

compile_args = [
    '-O3',
    '-Wno-cpp',
    '-g',
    '-Wno-write-strings',
    '-fpermissive',
    '-fPIC',
    '-std=c++11',
]

sources = [
    'Cython/' + 'slvs.pyx',
    src_path + 'util.cpp',
    src_path + 'entity.cpp',
    src_path + 'expr.cpp',
    src_path + 'constrainteq.cpp',
    src_path + 'constraint.cpp',
    src_path + 'system.cpp',
    src_path + 'lib.cpp',
]

if system() == 'Windows':
    # Avoid compile error with CYTHON_USE_PYLONG_INTERNALS.
    # https://github.com/cython/cython/issues/2670#issuecomment-432212671
    macros.append(('MS_WIN64', None))
    # Disable format warning
    compile_args.append('-Wno-format')

    # Solvespace arguments
    macros.append(('WIN32', None))

    # Platform sources
    sources.append(platform_path + 'w32util.cpp')
    sources.append(platform_path + 'platform.cpp')
else:
    sources.append(platform_path + 'unixutil.cpp')

setup(
    name="python_solvespace",
    # version="3.0.0",
    author=__author__,
    author_email=__email__,
    description="Python library of Solvespace",
    long_description=long_description,
    url="https://github.com/solvespace/solvespace",
    packages=find_packages(),
    ext_modules=[Extension(
        "slvs",
        sources=sources,
        language="c++",
        include_dirs=['include', src_path, platform_path],
        define_macros=macros,
        extra_compile_args=compile_args
    )],
    setup_requires=[
        'setuptools>=18.0',
        'wheel',
        'cython',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ]
)

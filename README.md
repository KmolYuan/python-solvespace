[![Build status](https://ci.appveyor.com/api/projects/status/b2o8jw7xnfqghqr5?svg=true)](https://ci.appveyor.com/project/KmolYuan/python-solvespace)
[![Build status](https://travis-ci.org/KmolYuan/python-solvespace.svg)](https://travis-ci.org/KmolYuan/python-solvespace)
![OS](https://img.shields.io/badge/OS-Windows%2C%20Mac%20OS%2C%20Ubuntu-blue.svg)
[![GitHub license](https://img.shields.io/badge/license-AGPLv3-blue.svg)](https://raw.githubusercontent.com/KmolYuan/python-solvespace/master/LICENSE)

Python Solvespace
===

Python library from solver of Solve Space. 

Use for academic research and learning.

Feature for CDemo and Python interface can see [here](https://github.com/KmolYuan/python-solvespace/blob/master/Cython/DOC.txt).

Requirement
===

1. [GNU Make] (Windows)

1. [Cython]

Build and Test
===

Build or clean the library:

```bash
make
make clean
```

Run unit test:

```bash
python test_slvs.py
```

[GNU Make]: https://sourceforge.net/projects/mingw-w64/files/latest/download?source=files
[Cython]: https://cython.org/

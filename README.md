[![Build Status](https://travis-ci.org/KmolYuan/python-solvespace.svg)](https://travis-ci.org/KmolYuan/python-solvespace)
![OS](https://img.shields.io/badge/OS-Linux%2C%20Windows-blue.svg)
[![GitHub license](https://img.shields.io/badge/license-AGPLv3-blue.svg)](https://raw.githubusercontent.com/KmolYuan/python-solvespace/master/LICENSE)

Python Solvespace
===

Python library from solver of Solve Space. 

Use for academic research and learning.

There hasn't any Solvespace main program but Makefile in the `exposed` folder (With two OS version).

Feature for CDemo and Python interface can see [Here](http://project.mde.tw/blog/slvs-library-functions.html) in English.

Or see [Here](http://project.mde.tw/blog/slvs-cheng-shi-ku-han-shi.html) in Chinese.

And there are some code and Solvespace drawing (Also include COMPILED library files) in OS (Windows and Ubuntu) folder.

Requirement
===

1. [GNU Make] (Windows)

1. [SWIG]

1. python3-dev (Ubuntu package)

Ubuntu
---

First, install SWIG. This tool kit can make a Python bundle with C/C++ library.

If your not, install python development kit.

```bash
sudo apt install swig python3-dev
```

Windows
---

Download and install [SWIG](http://www.swig.org/download.html).

Build
===

```bash
make
```

And take out this files:

* _slvs.pyd or _slvs.so
* slvs.py
* libslvs.so

[GNU Make]: https://sourceforge.net/projects/mingw-w64/files/latest/download?source=files
[SWIG]: http://www.swig.org/download.html

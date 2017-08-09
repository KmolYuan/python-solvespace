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

Some conflicts between the Microsoft C Language and Python.

You need change a few of Python files to avoid these conflicts.

But you can be assured that the changes won't cause any negative impact.

**Python development**

If your Python doesn't have development library, like `libpython35.a`, using `gendef` to generate it.

First copy `python3x.dll` to `where_your_python\libs` folder.

Then using this command:

```bash
gendef python3x.dll
dlltool --dllname python3x.dll --def python3x.def --output-lib libpython3x.a
```

And then adjust source code about Visual C. Find this code in `where_your_python\include\pyconfig.h`.

```c
#ifdef _WIN64
#define MS_WIN64
#endif
```

Cut them and paste **Above** this:

```c
#ifdef _MSC_VER
```

Find this code in `where_your_python\Lib\distutils\cygwinccompiler.py`:

```python
#with MSVC 7.0 or later.
self.dll_libraries = get_msvcr()
```

Commit `self.dll_libraries = get_msvcr()`.

**`math.h` conflict with `pyconfig.h`**

You will definitely get warning with `_hypot` in `pyconfig.h`, and you should do this step.

In `where_your_python\include\pyconfig.h`, find this:

```c
#define hypot _hypot
```

Edit it to this:

```c
#ifndef _MATH_H_
#define hypot _hypot
#endif
```

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

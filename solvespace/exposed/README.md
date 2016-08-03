Library Files
===

1. `_slvs.pyd` or `_slvs.so`

1. `slvs.py`

1. `libslvs.so`

1. `slvs_solid.py` (If want to use it)

1. And your python program(s)

Anaconda Adjustment
===

Some conflicts between the C Language and Python.

You need change a few of Python files to avoid these conflicts.

But you can be assured that this 

libpython35.a
---

If you got a warning say can't find `libpython35`, or a lot of warning, such as:

`slvs_wrap.o: In function '_SWIG_Py_None': slvs_wrap.cxx:1446: undefined reference to '__imp__Py_RefTotal'`

1. Copy `Anaconda3\python35.dll` into `Anaconda3\libs` folder.

1. Download **gendef** and install it.

1. Use this command:

```
cd "where you put python"\Anaconda3\libs

gendef python35.dll

dlltool --dllname python35.dll --def python35.def --output-lib libpython35.a
```

1. In `\Anaconda3\include\pyconfig.h`, find this:

```
#ifdef _WIN64
#define MS_WIN64
#endif
```

1. Cut them **Above** this:

```
#ifdef _MSC_VER
```

1. In `\Anaconda3\Lib\distutils\cygwinccompiler.py`, find this:

```
#with MSVC 7.0 or later.
self.dll_libraries = get_msvcr()
```

1. Commit `self.dll_libraries = get_msvcr()`

`math.h` conflict with `pyconfig.h`
---

If you got a warning with `_hypot` in `pyconfig.h`, you should do this:

1. In `\Anaconda3\include\pyconfig.h`, find this: `＃define hypot _hypot`

1. Edit it to this:

```
#ifndef _MATH_H_
#define hypot _hypot
#endif
```
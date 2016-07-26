python-solvespace
=================

Python library from solver of Solve Space. 

Use for academic research and learning.

Project-files
=================

Put these files into a same folder (Or you can just use them):

````
solvespace/exposed/_slvs.pyd
solvespace/exposed/libslvs.so
solvespace/exposed/slvs.py
solvespace/exposed/Usage.py
````

Edit `Usage.py` to design a subject.

(You can reference `DOC.txt`!)

And then execute `python Usage.py` in Command Prompt of Windows.

So `slvs.py` will ask `_slvs.pyd` and `libslvs.so` to solve subject.

In Ubuntu, you need to rebuild `_slvs.pyd` to `_slvs.so`.

Original `_slvs.so` is not compatible with Linux OS.

＊Of crouse you need to install [Anaconda](https://www.continuum.io/downloads) within Python 3.

My using tools
=================

This project made by following tools. (But they are Win-version.)

Compiler
-------------

Netbeans IDE `8.1`

plugins:

````
Python

Python/Jython Sample Projects
````

Python
-------------

Anaconda 3 with Python `3.5.2`

Other Python version maybe not compatible for some libraries.

GNU
-------------

gcc and g++ (GCC) `6.1.0`

gendef `1.0.1346`

dlltool `2.26.20160125`

objdump `2.26.20160125`

SWIG
-------------

SWIG `3.0.10`
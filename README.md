python-solvespace
=================

Python library from solver of Solve Space. 

Use for academic research and learning.

Project-files
=================

Put those files into a same folder (Or you can just use them):

````
solvespace/exposed/_slvs.pyd
solvespace/exposed/libslvs.so
solvespace/exposed/slvs.py
solvespace/exposed/Usage.py
````

Edit `Usage.py` to design a subject.

(You can reference `DOC.txt`!)

And then execute `python Usage.py` in Commder of Windows.

So `slvs.py` will ask `_slvs.pyd` and `libslvs.so` to solve subject.

My using tools
=================

In Ubuntu, you need to rebuild `_slvs.pyd` to `_slvs.so`.

Original `_slvs.so` is not compatible with Linux OS.

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

Python `3.5.2`

GNU
-------------

gcc and g++ (GCC) `6.1.0`

gendef `1.0.1346`

dlltool `2.26.20160125`

objdump `2.26.20160125`

SWIG
-------------

SWIG `3.0.10`
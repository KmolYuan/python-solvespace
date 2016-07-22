python-solvespace
=================

Geometry constraint solver of SolveSpace as a Python library

The solver has been written by Jonathan Westhues. You can find more information
[on his page][solvespace-lib]. It is part of [SolveSpace][solvespace-cad], which
is a parametric 3d CAD program.

My contributions:

* making it work on Linux (only the library, not the whole program!)
* nice Python interface
* some helpers for use with SolidPython (OpenSCAD)

I'm going to use the Python library with [SolidPython][solidpython], so I have a
constraint solver for [OpenSCAD][openscad].

[solvespace-cad]: http://solvespace.com/index.pl
[solvespace-lib]: http://solvespace.com/library.pl
[solidpython]:    https://github.com/SolidCode/SolidPython
[openscad]:       http://www.openscad.org/


Build and install
-----------------

The repository contains all the code for SolveSpace. This is necessary because the
library referes to files in its parent directory. The library is in `solvespace/exposed`.
You can run `make` to build the library. You should put the files `slvs.py` and `_slvs.so`
into a Python library directory or next to your application, so Python can find them.

If you are not using Linux, you have to change the Makefile accordingly. You could also
use the build system that the SWIG documentation [suggests][distutils], as this should
work on all platforms.

[distutils]: http://www.swig.org/Doc1.3/SWIGDocumentation.html#Python_nn6

Usage
-----

Here is a simple example:

````python
from slvs import *

# create a system with up to 20 parameters, entities and constraints
# (If you use System(), you will get the default of 50 parameters, ...)
sys = System(20)

# A point, initially at (x y z) = (10 10 10)
p1 = Point3d(Param(10.0), Param(10.0), Param(10.0), sys)
# and a second point at (20 20 20)
p2 = Point3d(Param(20.0), Param(20.0), Param(20.0), sys)
# and a line segment connecting them.
LineSegment3d(p1, p2)

# The distance between the points should be 30.0 units.
Constraint.distance(30.0, p1, p2)

# Let's tell the solver to keep the second point as close to constant
# as possible, instead moving the first point.
sys.set_dragged(p2)

# Now that we have written our system, we solve.
sys.solve()

if (sys.result == SLVS_RESULT_OKAY):
    print ("okay; now at (%.3f %.3f %.3f)\n" +
           "             (%.3f %.3f %.3f)") % (
            sys.get_param(0).val, sys.get_param(1).val, sys.get_param(2).val,
            sys.get_param(3).val, sys.get_param(4).val, sys.get_param(5).val)
    print "%d DOF" % sys.dof
else:
    print "solve failed"
````

Have a look at `CDemo.c` and `test.py`. They contain that example and another one. You can
use the raw C API from Python, but I suggest that you use the wrapper classes. `test.py`
uses both of them because it is meant to test the program.

TODO
----

* Integrate better with SolidPython.
* Find info about the other constraints and implement them.
* Clean up the code: remove all files that the library doesn't need.
* Make it build on all (or most) platforms.

License
-------

SolveSpace:<br>
"SolveSpace is distributed under the **GPLv3**, which permits most use in free software but
generally forbids linking the library with proprietary software. If you're interested in
the latter, then SolveSpace is also available for licensing under typical commercial terms;
please contact me for details."
(see [here](http://solvespace.com/library.pl))

You can use my parts of the code under GPLv3, as well. If the author of SolveSpace permits
use under another license (probably commercial), you may use my parts of the code under the
3-clause BSD license. In that case, you should add appropriate copyright headers to all files.

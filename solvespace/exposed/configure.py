import sys
import platform
import os.path

py_version = sys.version[0:sys.version.find(" ")]
py_nm = py_version[0:3]
py_locate = [i for i in sys.path]
system_type = platform.system()
system_name = platform.dist()[0]
system_version = platform.dist()[1]
system_machine = platform.machine()

def file_check():
    print(str(os.path.isfile('../solvespace.h'))+' | ../solvespace.h')
    print(str(os.path.isfile('../dsc.h'))+' | ../dsc.h')
    print(str(os.path.isfile('../sketch.h'))+' | ../sketch.h')
    print(str(os.path.isfile('../expr.h'))+' | ../expr.h')
    print(str(os.path.isfile('./slvs.h'))+' | ./slvs.h')
    print(str(os.path.isfile('../entity.cpp'))+' | ../entity.cpp')
    print(str(os.path.isfile('../expr.cpp'))+' | ../expr.cpp')
    print(str(os.path.isfile('../constrainteq.cpp'))+' | ../constrainteq.cpp')
    print(str(os.path.isfile('../system.cpp'))+' | ../system.cpp')
    print(str(os.path.isfile('./lib.cpp'))+' | ./lib.cpp')
    print(str(os.path.isfile('./slvs_python.hpp'))+' | ./slvs_python.hpp')
    print(str(os.path.isfile('./slvs.i'))+' | ./slvs.i')
    n = (os.path.isfile('../solvespace.h') and os.path.isfile('../dsc.h') and os.path.isfile('../sketch.h') and
         os.path.isfile('../expr.h') and os.path.isfile('./slvs.h') and os.path.isfile('../entity.cpp') and 
         os.path.isfile('../expr.cpp') and os.path.isfile('../constrainteq.cpp') and os.path.isfile('../system.cpp') and
         os.path.isfile('./lib.cpp') and os.path.isfile('./slvs_python.hpp') and os.path.isfile('./slvs.i')
         )
    return n

def build_Makefile():
    Makefile_script = "#Python Solvespace Makefile"
    if platform.system().lower()=="windows": Makefile_script += """
WIN_DEFINES = -D_WIN32_WINNT=0x500 -D_WIN32_IE=0x500 -DWIN32_LEAN_AND_MEAN
"""
    Makefile_script += """
DEFINES = -DISOLATION_AWARE_ENABLED -DLIBRARY -DDLL_EXPORT
CFLAGS  = -I../extlib -I../../common/win32 -I. -I.. -D_DEBUG -D_CRT_SECURE_NO_WARNINGS -O2 -g -Wno-write-strings -fpermissive
HEADERS = ../solvespace.h \
../dsc.h \
../sketch.h \
../expr.h \
slvs.h

OBJDIR = ../obj

SSOBJS = $(OBJDIR)/util.obj \
$(OBJDIR)/entity.obj \
$(OBJDIR)/expr.obj \
$(OBJDIR)/constrainteq.obj \
$(OBJDIR)/system.obj

W32OBJS = $(OBJDIR)/w32util.obj
LIBOBJS = $(OBJDIR)/lib.obj

#LIBS = user32.lib gdi32.lib comctl32.lib advapi32.lib shell32.lib
LIBS = 

CFILES = ../win32/w32util.cpp \
../entity.cpp \
../expr.cpp \
../constrainteq.cpp \
../system.cpp \
lib.cpp

OFILES = $(SSOBJS) $(LIBOBJS) $(W32OBJS) $(LIBS)
OWRAP = $(OBJDIR)/slvs_wrap.o
CWRAP = slvs_wrap.cxx
CXX = g++
PYTHONDLL = _slvs.pyd
PYTHONSO = _slvs.so
CSO = libslvs.so
CDEMO = cdemo
CDEMOEXE = CDemo.exe
"""
    if platform.system().lower()=="windows": Makefile_script += """
SWIG = \"W:\SWIG\swig.exe\"
PYTHON = \"W:\Anaconda3\python.exe\"
PYTHONLIB = -LW:/Anaconda3/libs -lPython"""+py_nm.replace('.', '')+"""
PYTHONINCLUDE = -IW:/Anaconda3/include

all: $(CSO) $(CDEMO) $(PYTHONDLL)
\t@cp -f --target-directory=W:/tmp/workplace/exposed/ _slvs.pyd libslvs.so slvs.py
\t@cp -f --target-directory=../../Windows _slvs.pyd libslvs.so slvs.py
\t@echo Complete
"""
    else: Makefile_script += """
SWIG = swig
PYTHON = python3
PYTHONLIB = -L/usr/lib/python"""+py_nm+"""/config-"""+py_nm+"""m-x86_64-linux-gnu/ -lpython"""+py_nm+"""m
PYTHONINCLUDE = -I/usr/include/python"""+py_nm+"""/

all: $(CSO) $(CDEMO) $(PYTHONSO)
\t@cp -f --target-directory=../../Ubuntu/ _slvs.so libslvs.so slvs.py
\t@echo Complete
"""
    Makefile_script += """
SONAME = -Wl,-soname,$(PYTHONSO) -o $(PYTHONSO)
DEFLIB = -Wl,--output-def,libslvs.def,--out-implib,libslvs.lib

VPATH = .. \
../win32
"""
    Makefile_script += """
test-python: slvs.py test.py
\t@echo \"$@\"
\t@echo test
\t@$(PYTHON) test.py

clean:
\t@rm -f $(OBJDIR)/*.o*
\t@rm -f $(CDEMO)
\t@rm -f $(CDEMOEXE)
\t@rm -f *.so*
\t@rm -f slvs.py
\t@rm -f $(CWRAP)
\t@rm -f *.exe
\t@rm -f *.a
\t@rm -f *.dll
\t@rm -f *.pyd

.SECONDEXPANSION:

$(CSO): $(OFILES)
\t@echo --------------------------------
\t@echo Dynamic link library: \"$@\"
\t$(CXX) -shared -o $@ $^
\t@echo --------------------------------
"""
    if platform.system().lower()=="windows": Makefile_script += """
$(PYTHONDLL): $(OFILES) $(OWRAP)
\t@echo --------------------------------
\t@echo Dynamic link library: "$@"
\t$(CXX) -shared -o $@ $(DEFLIB) $^ $(PYTHONLIB) -L. -l:$(CSO)
\t@echo --------------------------------

$(CDEMOEXE): CDemo.c $(CSO)
\t@echo ================================
\t@echo Executable files: "$@"
\t@$(CXX) $(CFLAGS) -o $@ $< -L. -l:$(CSO)
\t@echo ================================
"""
    else: Makefile_script += """
$(PYTHONSO): $(OFILES) $(OWRAP)
\t@echo --------------------------------
\t@echo Dynamic link library: "$@"
\t$(CXX) -shared -o $@ $^ $(PYTHONLIB)
\t@echo --------------------------------

$(CDEMO): CDemo.c $(CSO)
\t@echo ================================
\t@echo Executable files: "$@"
\t@$(CXX) $(CFLAGS) -o $@ $< -L. -l:$(CSO)
\t@echo ================================
"""
    Makefile_script += """
$(OBJDIR)/%.obj: %.cpp $(HEADERS)
\t@echo object: "$@"
\t@$(CXX) -fPIC $(CFLAGS) $(DEFINES) -c -o $@ $<

$(CWRAP): slvs.i slvs_python.hpp $(CSO)
\t@echo SWIG: "$@"
\t@$(SWIG) -c++ -python -py3 -o $@ $<

$(OWRAP): $(CWRAP)
\t@echo object: "$@"
\t@$(CXX) -fPIC -I../extlib -I../../common/win32 -I. -I.. -O2 $(DEFINES) -c -o $@ $< $(PYTHONINCLUDE)
"""
    
    with open("./Makefile", 'w', newline="")as f:
        f.write(Makefile_script)
    print("done!")

if __name__=='__main__':
    print("System: "+platform.system())
    print("Python Version: "+py_version)
    if file_check():
        print("Files checked done.")
        build_Makefile()
    else: print("Files not exist.")
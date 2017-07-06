#Python Solvespace Makefile
DEFINES = -DISOLATION_AWARE_ENABLED -DLIBRARY -DDLL_EXPORT
CFLAGS  = -I../extlib -I../../common/win32 -I. -I.. -D_DEBUG -D_CRT_SECURE_NO_WARNINGS -O2 -g -Wno-write-strings -fpermissive
HEADERS = $(SRCDIR)/solvespace.h $(SRCDIR)/dsc.h $(SRCDIR)/sketch.h $(SRCDIR)/expr.h slvs.h

OBJDIR = ../obj
SRCDIR = ..
OFILES = $(OBJDIR)/util.obj $(OBJDIR)/entity.obj $(OBJDIR)/expr.obj $(OBJDIR)/constrainteq.obj $(OBJDIR)/system.obj $(OBJDIR)/w32util.obj $(OBJDIR)/lib.obj
VPATH = .. ../win32

all: solver cdemo wrap $(HEADERS)
	@echo Finish

test: slvs.py test.py
ifeq ($(OS),Windows_NT)
	python test.py
else
	python3 test.py
endif

clean:
ifeq ($(OS),Windows_NT)
	del $(OBJDIR)\*.o*
	del CDemo.exe
	del *.so
	del slvs.py
	del slvs_wrap.cxx
else
	rm -f $(OBJDIR)/*.o*
	rm -f cdemo
	rm -f *.so
	rm -f slvs.py
	rm -f slvs_wrap.cxx
endif

help:
	@echo ================================
	@echo Python Solvespace - Solvespace Library for Python Script
	@echo Copyright \(C\) 2016 Yuan Chang
	@echo E-mail: daan0014119@gmail.com
	@echo --------------------------------
	@echo Use this Makefile to build Solvespace Library,
	@echo with Linux or Windows platform and Python 3.
	@echo 
	@echo Command:
	@echo all:		Complete compilation process.
	@echo clean:	Clean all maked files.
	@echo test:	Test Library with your Python.
	@echo help:	Show this help message.
	@echo ================================

.SECONDEXPANSION:

solver: $(OFILES)
	@echo --------------------------------
	@echo Dynamic link library: libslvs.so
	g++ -shared -o libslvs.so $^
	@echo --------------------------------

wrap: $(OFILES) $(OBJDIR)/slvs_wrap.o
	@echo --------------------------------
ifeq ($(OS),Windows_NT)
	@echo Dynamic link library: _slvs.pyd
	g++ -shared -o _slvs.pyd $^ \
-L$(shell python -c "from distutils import sysconfig;print(sysconfig.get_config_var('srcdir'))") \
-I$(shell python -c "from distutils import sysconfig;print(sysconfig.get_config_var('LDLIBRARY'))") -Wl,--output-def,libslvs.def,--out-implib,libslvs.lib -L. -l:libslvs.so
else
	@echo Dynamic link library: _slvs.so
	g++ -shared -o _slvs.so $^ \
-L$(shell python3 -c "from distutils import sysconfig;print(sysconfig.get_config_var('srcdir'))") \
-I$(shell python3 -c "from distutils import sysconfig;print(sysconfig.get_config_var('LDLIBRARY'))")
endif
	@echo --------------------------------

cdemo: CDemo.c solver
	@echo --------------------------------
ifeq ($(OS),Windows_NT)
	@echo Executable file: CDemo.exe
	g++ $(CFLAGS) -o CDemo.exe $< -L. -l:libslvs.so
else
	@echo Executable file: cdemo
	g++ $(CFLAGS) -o cdemo $< -L. -l:libslvs.so
endif
	@echo --------------------------------

$(OBJDIR)/%.obj: %.cpp
	@echo object: "$@"
	g++ -fPIC $(CFLAGS) $(DEFINES) -c -o $@ $<

$(OBJDIR)/slvs_wrap.o: slvs.i slvs_python.hpp.win slvs_python.hpp.ubuntu solver
	@echo SWIG: "$@"
ifeq ($(OS),Windows_NT)
	rename slvs_python.hpp.win slvs_python.hpp
else
	mv slvs_python.hpp.ubuntu slvs_python.hpp
endif
	swig -c++ -python -py3 -o slvs_wrap.cxx $<
	@echo object: slvs_wrap.cxx
ifeq ($(OS),Windows_NT)
	g++ -fPIC -I../extlib -I../../common/win32 -I. -I.. -O2 $(DEFINES) -c -o $@ slvs_wrap.cxx -I$(shell python -c "from distutils import sysconfig;print(sysconfig.get_python_inc())")
	rename slvs_python.hpp slvs_python.hpp.win
else
	g++ -fPIC -I../extlib -I../../common/win32 -I. -I.. -O2 $(DEFINES) -c -o $@ slvs_wrap.cxx -I$(shell python3 -c "from distutils import sysconfig;print(sysconfig.get_python_inc())")
	mv slvs_python.hpp slvs_python.hpp.ubuntu
endif

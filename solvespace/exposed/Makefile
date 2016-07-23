WIN_DEFINES = -D_WIN32_WINNT=0x500 -D_WIN32_IE=0x500 -DWIN32_LEAN_AND_MEAN
DEFINES = -DISOLATION_AWARE_ENABLED -DLIBRARY
# Use the multi-threaded static libc because libpng and zlib do; not sure if anything bad
# happens if those mix, but don't want to risk it.
#TODO -MT - multithread?
#TODO /Zi /EHs /O2 /GS-
CFLAGS  = -I../extlib -I../../common/win32 -I. -I.. -D_DEBUG -D_CRT_SECURE_NO_WARNINGS -O2 -g -Wno-write-strings -fpermissive
CFLAGS_SHARED = -fPIC -shared $(CFLAGS)

HEADERS = ../solvespace.h \
          ../dsc.h \
          ../sketch.h \
          ../expr.h \
          slvs.h \

OBJDIR = ../obj

SSOBJS = $(OBJDIR)/util.obj \
         $(OBJDIR)/entity.obj \
         $(OBJDIR)/expr.obj \
         $(OBJDIR)/constrainteq.obj \
         $(OBJDIR)/system.obj \

W32OBJS = $(OBJDIR)/w32util.obj \

LIBOBJS = $(OBJDIR)/lib.obj \

#LIBS = user32.lib gdi32.lib comctl32.lib advapi32.lib shell32.lib
LIBS = ../extlib/libpng.lib \
       ../extlib/zlib.lib \
       ../extlib/si/siapp.lib \

CFILES = ../win32/w32util.cpp \
        ../entity.cpp \
        ../expr.cpp \
        ../constrainteq.cpp \
        ../system.cpp \
        lib.cpp \

OFILES = $(SSOBJS) $(LIBOBJS) $(W32OBJS) $(LIBS)
OWRAP = $(OBJDIR)/slvs_wrap.obj
CWRAP = slvs_wrap.cpp
PYTHONSO = _slvs.so
LIBSO = libslvs.so

CXX = g++
SWIG = "W:\SWIG\swig.exe"
PYTHON = W:\Anaconda3\python.exe
PYTHONLIB = -LW:/Anaconda3/libs -lPython35
PYTHONINCLUDE = -IW:/Anaconda3/include
PYTHONA = W:/Anaconda3/libs/libpython35.a

VPATH = .. \
        ../win32 \

all: $(PYTHONSO) slvs.py test-c test-python

test-c: cdemo
	LD_LIBRARY_PATH=. ./cdemo

test-python: slvs.py Usage.py test.py
	@echo "$@"
	@echo Usage
	$(PYTHON) Usage.py
	@echo test
	$(PYTHON) test.py

clean:
	@rm -f $(OBJDIR)/*
	@rm -f cdemo.exe
	@rm -f $(LIBSO)
	@rm -f $(PYTHONSO)
	@rm -f slvs.py
	@rm -f $(CWRAP)
	@rm -f slvs.pyd

.SECONDEXPANSION:

$(LIBSO): $(OFILES)
	@echo "$@"
	@$(CXX) -shared -fPIC -o $@ $^

cdemo: CDemo.c $(LIBSO)
	@echo "$@"
	@$(CXX) $(CFLAGS) -o $@ $< -L. -l:$(LIBSO)

$(OBJDIR)/%.obj: %.cpp $(HEADERS)
	@echo object "$@"
	@$(CXX) -fPIC $(CFLAGS) $(DEFINES) -c -o $@ $<

$(CWRAP): slvs.i slvs_python.hpp $(LIBSO)
	@echo SWIG
	@$(SWIG) -c++ -python -py3 -o $@ $<

$(OWRAP): $(CWRAP)
	@echo object "$@"
	@$(CXX) -fPIC -D__WIN32__ -Wno-unused-but-set-variable -c -g -o $@ $< $(PYTHONINCLUDE)

$(PYTHONSO): $(OFILES) $(OWRAP)
	@echo "$@"
	@$(CXX) -shared -fPIC -o $@ $^ $(PYTHONLIB) -L. -lslvs
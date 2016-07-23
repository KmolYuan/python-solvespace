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
CWRAP = slvs_wrap.cxx
PYTHONSO = _slvs.so
LIBSO = libslvs.so
CDEMO = cdemo.exe

CXX = g++
SWIG = "W:\SWIG\swig.exe"
PYTHON = W:\Anaconda3\python.exe
PYTHONLIB = -LW:/Anaconda3/libs -lPython35
PYTHONINCLUDE = -IW:/Anaconda3/include
PYTHONA = W:/Anaconda3/libs/libpython35.a

VPATH = .. \
        ../win32 \

all: $(PYTHONSO) $(CDEMO) slvs.py
	@echo Complete

test-c: $(CDEMO)
	LD_LIBRARY_PATH=. ./$(CDEMO)

usage-python: slvs.py Usage.py
	@echo "$@"
	@echo Usage
	$(PYTHON) Usage.py

test-python: slvs.py test.py
	@echo "$@"
	@echo test
	$(PYTHON) test.py

clean:
	@rm -f $(OBJDIR)/*
	@rm -f $(CDEMO)
	@rm -f $(LIBSO)
	@rm -f $(PYTHONSO)
	@rm -f slvs.py
	@rm -f $(CWRAP)

.SECONDEXPANSION:

$(LIBSO): $(OFILES)
	@echo ---------------------------
	@echo Dynamic link library: "$@"
	@$(CXX) -shared -fPIC -o $@ $^
	@echo ---------------------------

$(CDEMO): CDemo.c $(LIBSO)
	@echo ===========================
	@echo Executable files: "$@"
	@$(CXX) $(CFLAGS) -o $@ $< -L. -l:$(LIBSO)
	@echo ===========================

$(OBJDIR)/%.obj: %.cpp $(HEADERS)
	@echo object: "$@"
	@$(CXX) -fPIC $(CFLAGS) $(DEFINES) -c -o $@ $<

$(CWRAP): slvs.i slvs_python.hpp $(LIBSO)
	@echo SWIG: "$@"
	@$(SWIG) -c++ -python -py3 -o $@ $<

$(OWRAP): $(CWRAP)
	@echo object: "$@"
	@$(CXX) -fPIC -D__WIN32__ -Wno-unused-but-set-variable -c -g -o $@ $< $(PYTHONINCLUDE)

$(PYTHONSO): $(OFILES) $(OWRAP)
	@echo ---------------------------
	@echo Dynamic link library: "$@"
	@$(CXX) -shared -fPIC -o $@ $^ $(PYTHONLIB) -L. -l:$(LIBSO)
	@echo ---------------------------
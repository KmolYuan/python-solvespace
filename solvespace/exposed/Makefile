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

CXX = g++

SWIG = "W:\swigwin-3.0.9\swig.exe"
PYTHON = W:\Anaconda3\python.exe
PYTHONLIB = -LW:/Anaconda3/libs -lPython35
PYTHONINCLUDE = -IW:/Anaconda3/include

VPATH = .. \
        ../win32 \

all: cdemo _slvs.so slvs.py
	LD_LIBRARY_PATH=. ./cdemo

test-python: _slvs.so slvs.py
	@echo test
	$(PYTHON) test.py
	@echo Usage
	$(PYTHON) Usage.py

clean:
	@rm -f $(OBJDIR)/*
	@rm -f cdemo.exe
	@rm -f libslvs.so
	@rm -f _slvs.so
	@rm -f slvs.py
	@rm -f slvs_wrap.cxx

.SECONDEXPANSION:

libslvs.so: $(SSOBJS) $(LIBOBJS) $(W32OBJS)
	@echo libslvs.so
	@$(CXX) -shared -fPIC -o $@ $^ $(LIBS)

cdemo: CDemo.c libslvs.so
	@echo cdemo
	@$(CXX) $(CFLAGS) -o $@ $< -L. -l:libslvs.so $(LIBS)

$(OBJDIR)/%.obj: %.cpp $(HEADERS)
	@echo obj "$@"
	@$(CXX) -fPIC $(CFLAGS) $(DEFINES) -c -o $@ $<

slvs.py slvs_wrap.cxx: slvs.i slvs_python.hpp
	@echo wrapCPP
	@$(SWIG) -c++ -python -py3 slvs.i

$(OBJDIR)/slvs_wrap.o: slvs_wrap.cxx slvs_python.hpp
	@echo wrapO
	@$(CXX) -fPIC -Wno-unused-but-set-variable -c -o $@ $< $(PYTHONINCLUDE)

_slvs.so: $(SSOBJS) $(LIBOBJS) $(W32OBJS) $(OBJDIR)/slvs_wrap.o
	@echo _slvs.so
	@$(CXX) -shared -o $@ $^ $(LIBS) $(PYTHONLIB) -L. -l:libslvs.so
# Python-Solvespace Makefile

DEFINES = -DISOLATION_AWARE_ENABLED -DLIBRARY -DDLL_EXPORT -D_hypot=hypot
CFLAGS  = -I. -Iinclude -Isrc -Isrc/platform -D_DEBUG -D_CRT_SECURE_NO_WARNINGS -O2 -g -Wno-write-strings -fpermissive -std=c++11

OBJDIR = obj

BASES = \
  util \
  entity \
  expr \
  constrainteq \
  constraint \
  system \
  lib

ifeq ($(OS), Windows_NT)
    SHELL = cmd
    CFLAGS += -DWIN32 -D_USE_MATH_DEFINES
    BASES += w32util platform
    WRAPPER = _slvs.pyd
    PYVER = $(shell python -c "from distutils import sysconfig;print(sysconfig.get_config_var('VERSION'))")
    PYINC = $(shell python -c "from distutils import sysconfig;print(sysconfig.get_python_inc())")
    PYLIB = $(shell python -c "from distutils import sysconfig;print(sysconfig.get_config_var('BINDIR'))")\libs
    DEFDLL = -Wl,--output-def,src/libslvs.def,--out-implib,src/libslvs.lib
else
    BASES += unixutil
    WRAPPER = _slvs.so
    PYVER = $(shell python3 -c "from distutils import sysconfig;print(sysconfig.get_config_var('VERSION'))")
    PYINC = $(shell python3 -c "from distutils import sysconfig;print(sysconfig.get_python_inc())")
    PYLIB = $(shell python3 -c "from distutils import sysconfig;print(sysconfig.get_config_var('srcdir'))")
    PYDIR = $(shell python3 -c "from distutils import sysconfig;print(sysconfig.get_config_var('LDLIBRARY'))")
endif

OBJS = $(addprefix $(OBJDIR)/,$(addsuffix .o,$(BASES)))

VPATH = src src/platform

.PHONY: _slvs clean

all: build

build: $(OBJDIR) libslvs.so $(WRAPPER)

clean:
ifeq ($(OS),Windows_NT)
	-rd /S /Q $(OBJDIR)
	-rd build /s /q
	-del *.so
	-del src\*.def
	-del src\*.lib
	-del src\*_wrap.cxx
	-del *.pyd
	-del src\slvs.cpp
	-del slvs.py
else
	-rm -fr $(OBJDIR)
	-rm -fr build
	-rm -f *.so
	-rm -f src/*_wrap.cxx
	-rm -f src/slvs.cpp
	-rm -f slvs.py
endif

.SECONDEXPANSION:

cython: setup.py
ifeq ($(OS),Windows_NT)
	python setup.py build_ext --inplace
else
	python3 setup.py build_ext --inplace
endif

$(OBJDIR):
ifeq ($(OS), Windows_NT)
	if not exist $(OBJDIR) mkdir $(OBJDIR)
else
	mkdir -p $(OBJDIR)
endif

$(OBJDIR)/%.o: %.cpp
	g++ -fPIC $(CFLAGS) $(DEFINES) -c -o $@ $<

libslvs.so: $(OBJS)
	g++ -shared -o $@ $^

src/slvs_wrap.cxx: src/slvs.i
	swig -c++ -python -py3 -outdir . -o $@ $<

$(OBJDIR)/slvs_wrap.o: slvs_wrap.cxx
	g++ -fPIC -I. -Iinclude -Isrc -Isrc/platform $(DEFINES) -c -o $@ $< -I$(PYINC)

$(WRAPPER): $(OBJDIR)/slvs_wrap.o
ifeq ($(OS),Windows_NT)
	g++ -shared -o $@ $(OBJS) $< -L. -Lsrc -l:libslvs.so -L$(PYLIB) -lpython$(PYVER) $(DEFDLL)
else ifeq ($(shell uname),Darwin)
	g++ -dynamiclib -o $@ $(OBJS) $< -L$(PYLIB) -lpython$(PYVER)m
else
	g++ -shared -o $@ $(OBJS) $< -L$(PYLIB) -I$(PYDIR)
endif

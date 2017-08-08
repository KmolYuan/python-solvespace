DEFINES = -DISOLATION_AWARE_ENABLED -DLIBRARY -DDLL_EXPORT
CFLAGS  = -I. -Iinclude -Isrc -Isrc/platform -D_DEBUG -D_CRT_SECURE_NO_WARNINGS -O2 -g -Wno-write-strings -fpermissive -std=c++11

OBJDIR = obj

OFILES = $(OBJDIR)/util.obj \
               $(OBJDIR)/entity.obj \
               $(OBJDIR)/expr.obj \
               $(OBJDIR)/constrainteq.obj \
               $(OBJDIR)/constraint.obj \
               $(OBJDIR)/system.obj \
               $(OBJDIR)/lib.obj

ifeq ($(OS), Windows_NT)
    CFLAGS += -DWIN32
    OFILES += $(OBJDIR)/w32util.obj
else
    OFILES += $(OBJDIR)/unixutil.obj
endif

HEADERS = src/solvespace.h src/platform/platform.h

VPATH = src src/platform

all: build
	@echo Finish

test: build
ifeq ($(OS),Windows_NT)
	python test.py
else
	python3 test.py
endif

clean:
ifeq ($(OS),Windows_NT)
	-rd /S /Q $(OBJDIR)
	-del *.so
	-del *.dll
	-del *.pyd
	-del cdemo
	-del slvs_wrap.cxx
	-del slvs.py
else
	-rm -fr $(OBJDIR)
	-rm -f *.so
	-rm -f cdemo
	-rm -f slvs_wrap.cxx
	-rm -f slvs.py
endif

.SECONDEXPANSION:

$(OBJDIR):
ifneq ($(wildcard $(OBJDIR)),)
else
	mkdir obj
endif

$(OBJDIR)/%.obj: %.cpp $(OBJDIR)
	g++ -fPIC $(CFLAGS) $(DEFINES) -c -o $@ $<

build: $(OFILES)
	g++ -shared -o libslvs.so $^
ifeq ($(OS),Windows_NT)
	rename slvs_python.hpp.win slvs_python.hpp
else
	mv slvs_python.hpp.ubuntu slvs_python.hpp
endif
	swig -c++ -python -py3 -o slvs_wrap.cxx slvs.i
ifeq ($(OS),Windows_NT)
	g++ -fPIC $(DEFINES) -c -o $(OBJDIR)/slvs_wrap.o slvs_wrap.cxx -I$(shell python -c "from distutils import sysconfig;print(sysconfig.get_python_inc())")
	rename slvs_python.hpp slvs_python.hpp.win
	g++ -shared -o _slvs.pyd $^ -L. -l:libslvs.so \
-L$(shell python -c "from distutils import sysconfig;print(sysconfig.get_config_var('BINDIR'))")\libs \
-lPython$(shell python -c "from distutils import sysconfig;print(sysconfig.get_config_var('VERSION'))") \
-Wl,--output-def,libslvs.def,--out-implib,libslvs.lib
else
	g++ -fPIC $(DEFINES) -c -o $(OBJDIR)/slvs_wrap.o slvs_wrap.cxx -I$(shell python3 -c "from distutils import sysconfig;print(sysconfig.get_python_inc())")
	mv slvs_python.hpp slvs_python.hpp.ubuntu
	g++ -shared -o _slvs.so $(OFILES) $(OBJDIR)/slvs_wrap.o \
-L$(shell python3 -c "from distutils import sysconfig;print(sysconfig.get_config_var('srcdir'))") \
-I$(shell python3 -c "from distutils import sysconfig;print(sysconfig.get_config_var('LDLIBRARY'))")
endif

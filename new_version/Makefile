DEFINES = -DISOLATION_AWARE_ENABLED -DLIBRARY -DDLL_EXPORT
CFLAGS  = -I. -Iinclude -Isrc -Isrc/platform -D_DEBUG -D_CRT_SECURE_NO_WARNINGS -O2 -g -Wno-write-strings -fpermissive -std=c++11

OBJDIR = obj

OFILES = $(OBJDIR)/util.o \
               $(OBJDIR)/entity.o \
               $(OBJDIR)/expr.o \
               $(OBJDIR)/constrainteq.o \
               $(OBJDIR)/constraint.o \
               $(OBJDIR)/system.o \
               $(OBJDIR)/lib.o

ifeq ($(OS), Windows_NT)
    CFLAGS += -DWIN32 -D_USE_MATH_DEFINES
    OFILES += $(OBJDIR)/w32util.o $(OBJDIR)/platform.o
else
    OFILES += $(OBJDIR)/unixutil.o
endif

HEADERS = src/solvespace.h src/platform/platform.h

VPATH = src src/platform

all: test

test: wrap
ifeq ($(OS),Windows_NT)
	python test.py
else
	python3 test.py
endif
	@echo Test done!

clean:
ifeq ($(OS),Windows_NT)
	-rd /S /Q $(OBJDIR)
	-del *.so
	-del *.def
	-del *.lib
	-del *.pyd
	-del slvs_wrap.cxx
	-del slvs.py
else
	-rm -fr $(OBJDIR)
	-rm -f *.so
	-rm -f slvs_wrap.cxx
	-rm -f slvs.py
endif

.SECONDEXPANSION:

$(OBJDIR):
ifneq ($(wildcard $(OBJDIR)),)
else
	mkdir obj
endif

$(OBJDIR)/%.o: %.cpp $(OBJDIR)
	g++ -fPIC $(CFLAGS) $(DEFINES) -c -o $@ $<

libslvs.so: $(OFILES)
	g++ -shared -o $@ $^

slvs_wrap.cxx: slvs.i libslvs.so
	swig -c++ -python -py3 -o $@ $<

$(OBJDIR)/slvs_wrap.o: slvs_wrap.cxx
ifeq ($(OS),Windows_NT)
	g++ -fPIC -I. -Iinclude -Isrc -Isrc/platform $(DEFINES) -c -o $@ $< \
-I$(shell python -c "from distutils import sysconfig;print(sysconfig.get_python_inc())")
else
	g++ -fPIC -I. -Iinclude -Isrc -Isrc/platform $(DEFINES) -c -o $@ $< \
-I$(shell python3 -c "from distutils import sysconfig;print(sysconfig.get_python_inc())")
endif

wrap: $(OFILES) $(OBJDIR)/slvs_wrap.o
ifeq ($(OS),Windows_NT)
	g++ -shared -o _slvs.pyd $^ -L. -l:libslvs.so \
-L$(shell python -c "from distutils import sysconfig;print(sysconfig.get_config_var('BINDIR'))")\libs \
-lPython$(shell python -c "from distutils import sysconfig;print(sysconfig.get_config_var('VERSION'))") \
-Wl,--output-def,libslvs.def,--out-implib,libslvs.lib
else
	g++ -shared -o _slvs.so $^ \
-L$(shell python3 -c "from distutils import sysconfig;print(sysconfig.get_config_var('srcdir'))") \
-I$(shell python3 -c "from distutils import sysconfig;print(sysconfig.get_config_var('LDLIBRARY'))")
endif
	@echo Finish

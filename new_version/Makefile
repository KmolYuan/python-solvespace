DEFINES = -DISOLATION_AWARE_ENABLED -DLIBRARY -DDLL_EXPORT
CFLAGS  = -Isrc -Isrc/platform -D_DEBUG -D_CRT_SECURE_NO_WARNINGS -O2 -g -Wno-write-strings -fpermissive -std=c++11

OBJDIR = obj

OFILES = $(OBJDIR)/util.obj \
               $(OBJDIR)/entity.obj \
               $(OBJDIR)/expr.obj \
               $(OBJDIR)/constrainteq.obj \
               $(OBJDIR)/constraint.obj \
               $(OBJDIR)/system.obj \
               $(OBJDIR)/lib.obj

ifeq ($(OS), Windows_NT)
    OFILES += $(OBJDIR)/w32util.obj
else
    OFILES += $(OBJDIR)/unixutil.obj
endif

HEADERS = src/solvespace.h src/platform/platform.h

VPATH = src src/platform

all: build
	@echo Finish

clean:
ifeq ($(OS),Windows_NT)
	-rd /S /Q $(OBJDIR)
	-del *.so
	-del *.dll
	-del *.pyd
else
	-rm -fr $(OBJDIR)
	-rm -f *.so
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

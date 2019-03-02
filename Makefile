# Python-Solvespace Makefile

ifeq ($(OS), Windows_NT)
    SHELL = cmd
endif

.PHONY: build clean

all: build

clean:
ifeq ($(OS),Windows_NT)
	-rd build /s /q
	-del *.so
	-del *.pyd
	-del Cython\*.cpp
else
	-rm -fr build
	-rm -f *.so
	-rm -f Cython/*.cpp
endif

build: setup.py
ifeq ($(OS),Windows_NT)
	python setup.py build_ext --inplace
else
	python3 setup.py build_ext --inplace
endif

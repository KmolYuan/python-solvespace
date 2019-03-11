# Python-Solvespace Makefile

# author: Yuan Chang
# copyright: Copyright (C) 2016-2019
# license: AGPL
# email: pyslvs@gmail.com

ifeq ($(OS), Windows_NT)
    SHELL = cmd
endif

.PHONY: build test clean

all: build

build: setup.py
ifeq ($(OS),Windows_NT)
	python $< build_ext -j0 --inplace
else
	python3 $< build_ext -j0 --inplace
endif

test: test_slvs.py build
ifeq ($(OS),Windows_NT)
	python $<
else
	python3 $<
endif

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

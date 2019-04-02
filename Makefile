CC = gcc
PY = python
RM = rm -rf

.PHONY: all build build_ext dist bdist bdist_wheel sdist upload clean run

all: build

dist: sdist

build: build_ext

bdist: bdist_wheel

build_ext bdist_wheel sdist:
	$(PY) setup.py $@

upload: dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*.tar.gz --verbose

clean:
	$(PY) setup.py clean -a
	$(RM) build dist pyckip.egg-info

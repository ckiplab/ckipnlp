PY = python
RM = rm -rf
LINT = pylint --rcfile=./.pylintrc

.PHONY: all dist bdist bdist_wheel sdist test lint upload clean

all: dist

dist: sdist

sdist test:
	$(PY) setup.py $@

lint:
	$(LINT) ckipnlp

upload: dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*.tar.gz --verbose

clean:
	$(PY) setup.py clean -a
	$(RM) build dist *.egg-info *.so __pycache__

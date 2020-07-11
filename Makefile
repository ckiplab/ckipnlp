PY = python3
RM = rm -rf
LINT = pylint --rcfile=./.pylintrc
TWINE = twine

.PHONY: all check dist sdist testall test lint doc upload clean

all: dist check testall

dist: sdist bdist_wheel

testall: test lint

sdist bdist_wheel test:
	$(PY) setup.py $@

lint:
	$(LINT) ckipnlp

check:
	$(TWINE) check dist/*

doc:
	( cd docs ; make clean ; make html )

upload: dist check
	ls dist/*
	$(TWINE) upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose

clean:
	( cd docs ; make clean )
	$(PY) setup.py clean -a
	$(RM) build dist *.egg-info *.so __pycache__

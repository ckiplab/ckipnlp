PY = python3
RM = rm -rf
TWINE = twine
TOX = tox
LINT = pylint --rcfile=./.pylintrc

.PHONY: all check dist sdist test tox lint doc upload clean

all: dist check testall

dist: sdist bdist_wheel

test: tox lint

sdist bdist_wheel:
	$(PY) setup.py $@

tox:
	$(TOX)

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

PY = python3
RM = rm -rf
TWINE = twine
TOX = tox
LINT = pylint --rcfile=./.pylintrc

.PHONY: all check dist sdist test tox tox-v tox-report lint doc upload clean

all: dist check test

dist: sdist bdist_wheel

test: tox lint

sdist bdist_wheel:
	$(PY) setup.py $@

tox:
	- $(TOX) -p -f py36,py37,py38

tox-v:
	- $(TOX)

tox-report:
	- $(TOX) -p -f clean,py36,report -- --cov-report=term-missing --cov-append
	python3.7 -m http.server --directory .test/htmlcov/ 3000

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
	- ( cd docs ; make clean )
	- $(PY) setup.py clean -a
	- $(TOX) -e clean
	- $(RM) build dist .tox .test .lookup __pycache__

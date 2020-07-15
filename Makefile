PY = python3
RM = rm -rf
TWINE = twine
TOX = tox
LINT = pylint --rcfile=./.pylintrc

.PHONY: all check dist sdist test tox tox-report lint doc upload clean

all: dist check test

dist: sdist bdist_wheel

test: tox lint

sdist bdist_wheel:
	$(PY) setup.py $@

tox:
	- $(TOX) -p -e py{36,37,38}
	- $(TOX) -e py36-pipeline -- -v

tox-seq:
	- $(TOX)

tox-report:
	- $(TOX) -p -e clean,py36,report -- --cov-report=html
	# - $(TOX) -p -e clean,py{36,37,38},report -- --cov-report=term-missing --cov-append
	python3.7 -m http.server --directory htmlcov/ 3000

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
	- $(RM) build dist .tox .coverage htmlcov *.egg-info *.so __pycache__

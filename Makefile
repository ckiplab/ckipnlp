PY = python
RM = rm -rf
LINT = pylint --rcfile=./.pylintrc

.PHONY: all check dist sdist test lint doc upload clean

all: dist check

dist: sdist

sdist test:
	$(PY) setup.py $@

check:
	$(PY) setup.py check -r -s

lint:
	$(LINT) ckipnlp

doc:
	( cd docs ; make clean ; make html )

upload: dist check
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*.tar.gz --verbose

clean:
	( cd docs ; make clean )
	$(PY) setup.py clean -a
	$(RM) build dist *.egg-info *.so __pycache__

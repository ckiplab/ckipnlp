RM = rm -rf
TOX = tox

.PHONY: tox tox-v tox-report clean

tox:
	NO_COV= $(TOX) -p -f py36,py37,py38

tox-v:
	NO_COV= $(TOX) -f py36,py37,py38 -- -v

tox-report:
	- $(TOX) -p -f clean,py36,report -- --cov-append
	python3.7 -m http.server --directory .test/htmlcov/ 3000

clean:
	- $(RM) .tox .test .lookup

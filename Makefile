h: help

help:
	@echo "Options:"
	@echo "format: Reformat all python files with black"
	@echo "tests: Run tests with nosetest"
	@echo "verbose_tests: Run tests with nosetest -v"

f: format
t: test
v: verbose_tests

format: format_code format_tests

format_code:
	black pdcrier/*.py
	black bin/*

format_tests:
	black tests/*.py

tests: test
test:
	nosetests

verbose_test: verbose_tests
verbose_tests:
	nosetests -v

venv:
	virtualenv venv
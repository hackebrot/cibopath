.PHONY: clean-tox clean-py clean-build develop test

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-py - remove Python file artifacts"
	@echo "clean-tox - remove tox file artifacts"
	@echo "clean - remove all file artifacts"
	@echo "develop - install development dependencies"
	@echo "test - install dev dependencies and run tests"

clean: clean-tox clean-build clean-py

clean-tox:
	rm -rf .tox/

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean-py:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

develop:
	pip install -r requirements-dev.txt

test: develop
	tox

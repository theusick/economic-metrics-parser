PYTHON ?= python3.9

PROJECT_SOURCE_DIR ?= parser


help:
	@echo 'The following commands can be used.'
	@echo 'make precommit' - Run precommit check without commiting
	@echo 'make clean	   - Remove files created by distutils'
	@echo 'make devenv	   - Create & setup development virtual environment'
	@echo 'make formatter  - Runs black on src'
	@echo 'make sdist	   - Make source distribution'
	@exit 0

precommit:
	pre-commit run --all-files

clean:
	rm -fr *.egg-info dist
	find . -name '__pycache__' | xargs rm -rf

devenv: clean
	rm -rf venv
	$(PYTHON) -m venv venv
	venv/bin/pip install -U pip

formatter:
	$(PYTHON) -m black $(PROJECT_SOURCE_DIR)

sdist: clean
	$(PYTHON) setup.py sdist

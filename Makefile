VENV_FOLDER ?= .venv
ifeq ($(OS),Windows_NT)
	VENV_BIN_FOLDER ?= ${VENV_FOLDER}\Scripts
	VENV_ACTIVATE ?= ${VENV_BIN_FOLDER}\activate
	VENV_PYTHON ?= ${VENV_BIN_FOLDER}\python
	PYTHON ?= python
	OS_detected := win
else
	VENV_BIN_FOLDER ?= ${VENV_FOLDER}/bin
	VENV_ACTIVATE ?= ${VENV_BIN_FOLDER}/activate
	VENV_PYTHON ?= ${VENV_BIN_FOLDER}/python3
	PYTHON ?= python3
	OS_detected := unix
endif

PYTHON_SCRIPT ?= safaricsv2pdf.py
EXAMPLES_FOLDER ?= examples
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell ${PYTHON} --version 2>&1)))
python_version_major := $(word 1,${python_version_full})

.PHONY: all build build-mac build-win check check.python.2 check.python.3 clean clean-all clean-pyc deps examples \
		list unix.build unix.clean unix.clean-all unix.clean-pyc unix.deps unix.examples venv win.build win.clean \
		win.clean-all win.clean-pyc win.deps win.examples

all:
	@$(MAKE) -s build

list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

check.python.2:
	@echo "Python version not supported, please use Python 3"
	@exit 1

check.python.3:
	@echo "Python version: OK"

check: check.python.${python_version_major}

venv: check
	@echo "Creating virtualenv..."
	@${PYTHON} -m venv ${VENV_FOLDER}

deps: venv
	@echo "Installing dependencies..."
	@$(MAKE) -s ${OS_detected}.deps

win.deps:
	@${VENV_ACTIVATE} && pip install -qU -r requirements.txt

unix.deps:
	@source ${VENV_ACTIVATE} && pip install -qU -r requirements.txt

build: deps
	@echo "Building executable..."
	@$(MAKE) -s ${OS_detected}.build
	@echo "Done."
	@exit 0

win.build:
	@${VENV_ACTIVATE} && pyinstaller --clean --log-level ERROR safaricsv2pdf.win.spec

unix.build:
	@source ${VENV_ACTIVATE} && pyinstaller --clean --log-level ERROR safaricsv2pdf.mac.spec

clean: clean-pyc
	@$(MAKE) -s ${OS_detected}.clean

win.clean:
	@if exist dist rmdir /s /q dist
	@if exist build rmdir /q build
	@del /q /s ${EXAMPLES_FOLDER}\*.pdf 1>nul 2>nul

unix.clean:
	@rm -rf dist build ${EXAMPLES_FOLDER}/*.pdf

clean-all: clean
	@$(MAKE) -s ${OS_detected}.clean-all

win.clean-all:
	@if exist .venv rmdir /s /q .venv
	@if exist __pycache__ rmdir /s /q __pycache__

unix.clean-all:
	@rm -rf .venv __pycache__

clean-pyc:
	@$(MAKE) -s ${OS_detected}.clean-pyc

win.clean-pyc:
	@del /s *.pyc >nul 2>&1

unix.clean-pyc:
	@rm -f *.pyc

examples: deps
	@$(MAKE) -s ${OS_detected}.examples

win.examples:
	@${VENV_ACTIVATE} && ${PYTHON} ${PYTHON_SCRIPT} ${EXAMPLES_FOLDER}

unix.examples:
	@source ${VENV_ACTIVATE} && ${PYTHON} ${PYTHON_SCRIPT} ${EXAMPLES_FOLDER}

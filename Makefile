PYTHON = python3
SRC_FILES = $(wildcard src/**/*.py)

build: dist 

dist: $(SRC_FILES)
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build

.PHONY: test
test:
	$(PYTHON) -m unittest discover -v

.PHONY: clean
clean:
	rm -rf dist

.PHONY: install
install: # only there for testing purposes
	pip install -r requirements.txt
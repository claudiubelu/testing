.PHONY: all-build-images all-publish-images push-manifests clean clean-build clean-pyc clean-test coverage dist docs help install lint lint/flake8 lint/black
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

TAG ?= 0.1.0
REGISTRY ?= docker.io

# Other OSes that could be supported: windows, darwin.
OS ?= linux

# Other architectures that can be supported: arm, arm64, ppc64le, s390x.
ARCH ?= amd64

# The output type could either be docker (local), or registry.
OUTPUT_TYPE ?= docker

ALL_OS = linux
ALL_ARCH = amd64 arm arm64
ALL_OS_ARCH = $(foreach os, $(ALL_OS), $(foreach arch, ${ALL_ARCH}, $(os)-$(arch)))

WORKER_IMAGE = $(REGISTRY)/sobolanism-worker:$(TAG)
CLIENT_IMAGE = $(REGISTRY)/sobolanism-client:$(TAG)

# Target build an images for a particular OS and Architecture.
build-images:
	docker buildx build --pull --output=type=$(OUTPUT_TYPE) --platform $(OS)/$(ARCH) \
		-t $(WORKER_IMAGE)-$(OS)-$(ARCH) -f docker/worker/Dockerfile .
	docker buildx build --pull --output=type=$(OUTPUT_TYPE) --platform $(OS)/$(ARCH) \
		-t $(CLIENT_IMAGE)-$(OS)-$(ARCH) -f docker/client/Dockerfile .

# split words on hyphen, access by 1-index
word-hyphen = $(word $2,$(subst -, ,$1))

# This will recursively call make build-images for a particular OS and Arch.
sub-build-image-%:
	$(MAKE) OUTPUT_TYPE=$(call word-hyphen,$*,1) OS=$(call word-hyphen,$*,2) ARCH=$(call word-hyphen,$*,3) build-images

# Setup QEMU.
register-qemu-static:
	${sudo} docker run --rm --privileged tonistiigi/binfmt:latest --install all

# Trigger the image building process without pushing to the registry.
all-build-images-docker: register-qemu-static $(addprefix sub-build-image-docker-,$(ALL_OS_ARCH))

# Trigger the image building process and pushing them to the registry.
all-build-images-registry: register-qemu-static $(addprefix sub-build-image-registry-,$(ALL_OS_ARCH))

all-build-images: all-build-images-docker
all-publish-images: all-build-images-registry

push-manifests: all-publish-images
	docker manifest create --amend $(WORKER_IMAGE) $(shell echo $(ALL_OS_ARCH) | sed -e "s~[^ ]*~$(WORKER_IMAGE)\-&~g")
	set -x; for os in $(ALL_OS); do for arch in $(ALL_ARCH); do docker manifest annotate --os $${os} --arch $${arch} $(WORKER_IMAGE} $(WORKER_IMAGE)-$${os}-$${arch}; done; done
	docker manifest push --purge $(WORKER_IMAGE)
	docker manifest create --amend $(CLIENT_IMAGE) $(shell echo $(ALL_OS_ARCH) | sed -e "s~[^ ]*~$(CLIENT_IMAGE)\-&~g")
	set -x; for os in $(ALL_OS); do for arch in $(ALL_ARCH); do docker manifest annotate --os $${os} --arch $${arch} $(CLIENT_IMAGE} $(CLIENT_IMAGE)-$${os}-$${arch}; done; done
	docker manifest push --purge $(CLIENT_IMAGE)

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint/flake8: ## check style with flake8
	flake8 sobolanism tests
lint/black: ## check style with black
	black --check sobolanism tests

lint: lint/flake8 lint/black ## check style

test: ## run tests quickly with the default Python
	python setup.py test

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source sobolanism setup.py test
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/sobolanism.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ sobolanism
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

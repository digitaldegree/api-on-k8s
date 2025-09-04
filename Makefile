APP = $(notdir $(CURDIR))
TAG = $(shell echo "$$(date +%F)-$$(git rev-parse --short HEAD)")
DOCKER_REPO = ghcr.io/managedkaos


help:
	@echo "Run make <target> where target is one of the following..."
	@echo
	@echo "  all                      - run requirements, lint, test, and build"
	@echo "  requirements             - install runtime dependencies"
	@echo "  development-requirements - install development dependencies"
	@echo "  pre-commit-install       - install pre-commit hooks"
	@echo "  pre-commit-update        - update pre-commit hooks"
	@echo "  pre-commit-run           - run pre-commit on all files"
	@echo "  pre-commit-clean         - remove pre-commit hooks"
	@echo "  lint                     - run flake8, pylint, black, and isort checks"
	@echo "  black                    - format code with black"
	@echo "  isort                    - sort imports with isort"
	@echo "  test                     - run unit tests"
	@echo "  build                    - build docker container"
	@echo "  clean                    - clean up workspace and containers"

all: requirements pre-commit-run test build

setup: development-requirements pre-commit-install

pre-commit-install:
	pre-commit install
	detect-secrets scan > .secrets.baseline

pre-commit-update:
	pre-commit autoupdate

pre-commit-run:
	pre-commit run --all-files

x_pre-commit-clean:
	pre-commit uninstall

apply:
	kubectl apply -f ./config

requirements development-requirements lint fmt black isort test build clean:
	$(MAKE) -C ./src $@

.PHONY: help requirements lint black isort test build clean development-requirements pre-commit-install pre-commit-run pre-commit-clean

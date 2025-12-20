VERSION := 0.11.0

POETRY := bin/poetry/bin/poetry

PYTHON_FILES := $(shell git ls-files "*.py" ':!:whitelist.py')
PACKAGE_FILES := $(shell git ls-files "constcheck/*.py")
DOCS_FILES := $(shell git ls-files "docs/*.rst" "docs/*.md")

BUILD := dist/constcheck-$(VERSION)-py3-none-any.whl

ifeq ($(OS),Windows_NT)
	VENV := .venv/Scripts/activate
else
	VENV := .venv/bin/activate
endif

.PHONY: all
#: install development environment
all: .make/pre-commit

.PHONY: build
#: phony target for build
build: $(BUILD)

#: build and check integrity of distribution
$(BUILD): .make/doctest \
	coverage.xml \
	.make/format \
	docs/_build/html/index.html \
	.make/lint \
	.mypy_cache/CACHEDIR.TAG \
	docs/_build/linkcheck/output.json \
	docs/constcheck.rst
	@$(POETRY) run pyaud audit
	@$(POETRY) build
	@touch $@

.PHONY: publish
#: publish distribution
publish: $(BUILD)
	@$(POETRY) publish

.PHONY: test
#: test source
test: .make/doctest coverage.xml

#: generate documentation
docs/_build/html/index.html: $(VENV) \
	$(PYTHON_FILES) \
	$(DOCS_FILES) \
	CHANGELOG.md \
	.conform.yaml
	@$(POETRY) run $(MAKE) -C docs html

#: install poetry
$(POETRY):
	@curl -sSL https://install.python-poetry.org | \
		POETRY_HOME="$$(pwd)/bin/poetry" "$$(which python)" - --version 2.2.1
	@touch $@

#: generate virtual environment
$(VENV): $(POETRY) poetry.lock
	@[ ! $$(basename "$$($< env info --path)") = ".venv" ] \
		&& rm -rf "$$($< env info --path)" \
		|| exit 0
	@POETRY_VIRTUALENVS_IN_PROJECT=1 $< install
	@touch $@

#: install pre-commit hooks
.make/pre-commit: $(VENV)
	@$(POETRY) run pre-commit install \
		--hook-type pre-commit \
		--hook-type pre-merge-commit \
		--hook-type pre-push \
		--hook-type prepare-commit-msg \
		--hook-type commit-msg \
		--hook-type post-commit \
		--hook-type post-checkout \
		--hook-type post-merge \
		--hook-type post-rewrite
	@mkdir -p $(@D)
	@touch $@

.PHONY: clean
#: clean compiled files
clean:
	@find . -name '__pycache__' -exec rm -rf {} +
	@rm -rf .coverage
	@rm -rf .git/hooks/*
	@rm -rf .make
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
	@rm -rf .venv
	@rm -rf bin
	@rm -rf coverage.xml
	@rm -rf dist
	@rm -rf docs/_build

#: generate coverage report
coverage.xml: $(VENV) $(PACKAGE_FILES) $(TEST_FILES)
	@$(POETRY) run pytest --cov=constcheck --cov=tests \
		&& $(POETRY) run coverage xml

#: test code examples in documentation
.make/doctest: $(VENV) README.rst $(PYTHON_FILES) $(DOCS_FILES)
	@$(POETRY) run pytest docs README.rst --doctest-glob='*.rst'
	@mkdir -p $(@D)
	@touch $@

.PHONY: update-copyright
#: update copyright year in files containing it
update-copyright: $(VENV)
	@$(POETRY) run python3 scripts/update_copyright.py

#: run checks that format code
.make/format: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run black $(PYTHON_FILES)
	@$(POETRY) run flynt $(PYTHON_FILES)
	@$(POETRY) run isort $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

#: lint code
.make/lint: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run pylint --output-format=colorized $(PYTHON_FILES)
	@$(POETRY) run docsig $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

#: check typing
.mypy_cache/CACHEDIR.TAG: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run mypy $(PYTHON_FILES)
	@touch $@

#: generate whitelist of allowed unused code
whitelist.py: $(VENV) $(PACKAGE_FILES) $(TEST_FILES)
	@$(POETRY) run vulture --make-whitelist constcheck tests > $@ || exit 0

#: check for unused code
.make/unused: whitelist.py
	@$(POETRY) run vulture whitelist.py constcheck tests
	@mkdir -p $(@D)
	@touch $@

#: confirm links in documentation are valid
docs/_build/linkcheck/output.json: $(VENV) \
	$(PYTHON_FILES) \
	$(DOCS_FILES) \
	CHANGELOG.md \
	.conform.yaml
	@trap "rm -f $(@); exit 1" ERR; \
		{ \
			ping -c 1 constcheck.readthedocs.io >/dev/null 2>&1 \
			|| { echo "could not establish connection, skipping"; exit 0; }; \
			$(POETRY) run $(MAKE) -C docs linkcheck; \
		}

#: check dependencies are properly managed
.make/check-deps: $(VENV) $(PYTHON_FILES) pyproject.toml
	@$(POETRY) run deptry .
	@mkdir -p $(@D)
	@touch $@

#: poetry lock
poetry.lock: pyproject.toml
	@$(POETRY) lock
	@touch $@

.PHONY: deps-update
#: update dependencies
deps-update:
	@$(POETRY) update

#: make custom toc file
docs/constcheck.rst: $(VENV)
	@$(POETRY) run python scripts/update_toc.py
	@touch $@

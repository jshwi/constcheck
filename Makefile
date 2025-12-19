POETRY := bin/poetry/bin/poetry

ifeq ($(OS),Windows_NT)
	VENV := .venv/Scripts/activate
else
	VENV := .venv/bin/activate
endif

all: $(VENV) install-hooks
remove: remove-poetry remove-hooks remove-deps

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

install-pre-commit:
	@poetry run command -v pre-commit > /dev/null 2>&1 \
		|| poetry run pip --quiet install pre-commit

install-hooks: install-pre-commit
	@poetry run pre-commit install \
		--hook-type pre-commit \
		--hook-type pre-merge-commit \
		--hook-type pre-push \
		--hook-type prepare-commit-msg \
		--hook-type commit-msg \
		--hook-type post-commit \
		--hook-type post-checkout \
		--hook-type post-merge \
		--hook-type post-rewrite

remove-hooks: install-pre-commit
	@poetry run pre-commit uninstall \
		--hook-type pre-commit \
		--hook-type pre-merge-commit \
		--hook-type pre-push \
		--hook-type prepare-commit-msg \
		--hook-type commit-msg \
		--hook-type post-commit \
		--hook-type post-checkout \
		--hook-type post-merge \
		--hook-type post-rewrite

remove-deps:
	rm -rf $(shell dirname $(shell dirname $(shell poetry run which python)))

remove-poetry:
	@command -v poetry >/dev/null 2>&1 \
		|| curl -sSL https://install.python-poetry.org | python3 - --uninstall

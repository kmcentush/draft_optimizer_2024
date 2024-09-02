.PHONY: install
install:
	uv pip install --upgrade -e .

.PHONY: dev_install
dev_install:
	uv pip install --upgrade -e .[dev]
	pre-commit install

.PHONY: prd_compile
prd_compile:
	uv pip compile pyproject.toml -o requirements.txt --universal --upgrade

.PHONY: prd_install
prd_install:
	uv pip sync requirements.txt
	uv pip install -e . --no-deps

.PHONY: format
format:
	ruff format .
	ruff check . --fix
	pyright .

.PHONY: test_format
test_format:
	ruff format . --check
	ruff check .
	pyright .

.PHONY: pytest
pytest:
	pytest --cov-report term-missing --cov=src tests/ -s

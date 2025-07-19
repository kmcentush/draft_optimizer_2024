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
	ruff check . --fix
	ruff format .
	ty check .

.PHONY: test_format
test_format:
	ruff check .
	ruff format . --check
	ty check .

.PHONY: pytest
pytest:
	pytest --cov-report term-missing --cov=src tests/ -s

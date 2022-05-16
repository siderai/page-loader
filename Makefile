install:
	pip install poetry
	poetry install

package-install:
	poetry install
	rm -rf dist
	poetry build
	pip install --upgrade pip
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8

test:
	poetry run pytest -vv -o log_cli=true

test-cov:
	poetry run pytest --cov=page_loader --cov-report xml tests/

show-cov:
	poetry run pytest --cov=page_loader --cov-report term-missing

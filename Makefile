install:
	poetry install

package-install:
	poetry install
	poetry build
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 gendiff

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=loader --cov-report xml tests/

show-cov:
	poetry run pytest --cov=loader


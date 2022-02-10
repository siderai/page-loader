install:
	poetry install

package-install:
	poetry install
	poetry build
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 --ignore=F405,F403

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=page_loader --cov-report xml tests/

show-cov:
	poetry run pytest --cov=page_loader --cov-report term-missing

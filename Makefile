test:
	poetry run pytest --doctest-modules

lint:
	poetry run flake8

all:	lint test

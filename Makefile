SHELL := /bin/bash

init:
	python3 -m venv venv
	source venv/bin/activate && ( \
	pip install -r requirements.txt; \
	)

format:
	isort . --profile black -l 99
	black .

install-lint:
	python -m pip install --upgrade pip
	pip install -r requirements.txt  # needed for pytype
	pip install black isort flake8 pylint pytype mypy

lint:
	flake8 ./product ./shop ./transaction
	pylint ./product ./shop ./transaction
	# pytype ./product ./shop ./transaction
	mypy ./product ./shop ./transaction

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

super-user:
	python manage.py createsuperuser --username ananto
all: makemigrations migrate run

run:
	python3 src/manage.py runserver

build:
	docker build -t sport-app:1 .

down:
	docker compose down --remove-orphans

up:
	docker compose up -d

test:
	pytest

migrate:
	python src/manage.py migrate

makemigrations:
	python3 src/manage.py makemigrations
	sudo chown -R ${USER} src/app/migrations/

createsuperuser:
	python src/manage.py createsuperuser

collectstatic:
	python src/manage.py collectstatic --no-input

dev:
	python src/manage.py runserver localhost:8000

command:
	python3 src/manage.py ${c}

shell:
	python3 src/manage.py shell

debug:
	python3 src/manage.py debug

piplock:
	pipenv install
	sudo chown -R ${USER} Pipfile.lock

lint:
	isort .
	flake8 --config setup.cfg

check_lint:
	isort --check --diff .
	flake8 --config setup.cfg

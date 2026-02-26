install:
	uv sync

dev-install:
	uv sync --group dev

migrations:
	uv run python manage.py makemigrations

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --noinput

run:
	uv run python manage.py runserver

render-start:
	uv run gunicorn tengecash.wsgi

render-build:
	./build.sh
	uv run python manage.py migrate --noinput

build:
	./build.sh

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

test:
	uv run pytest --ds=tengecash.settings --reuse-db

coverage:
	uv run coverage run --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest --ds=tengecash.settings
	uv run coverage report --show-missing --skip-covered

ci-install:
	uv sync --group dev

ci-migrate:
	uv run python manage.py makemigrations --noinput && \
	uv run python manage.py migrate --noinput

ci-test:
	uv run coverage run --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest tengecash --ds=tengecash.settings --reuse-db
	uv run coverage xml
	uv run coverage report --show-missing --skip-covered

runbot:
	uv run python tengecash/bot_app/bot.py
install:
	poetry install --no-root

dev-install:
	poetry install --no-root

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

collectstatic:
	poetry run python manage.py collectstatic --noinput

run:
	poetry run python manage.py runserver

render-start:
	poetry run gunicorn qaltamda.wsgi  # Заменил tengecash на qaltamda

render-build:
	./build.sh
	# Миграции лучше оставить в Start Command на Render, но если нужно тут:
	poetry run python manage.py migrate --noinput

build:
	./build.sh

lint:
	poetry run ruff check

lint-fix:
	poetry run ruff check --fix

test:
	poetry run pytest --ds=qaltamda.settings --reuse-db

coverage:
	poetry run coverage run --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest --ds=qaltamda.settings
	poetry run coverage report --show-missing --skip-covered

ci-install:
	poetry install --no-root

ci-migrate:
	poetry run python manage.py makemigrations --noinput && \
	poetry run python manage.py migrate --noinput

ci-test:
	poetry run coverage run --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest --ds=qaltamda.settings --reuse-db
	poetry run coverage xml
	poetry run coverage report --show-missing --skip-covered

runbot:
	poetry run python qaltamda/bot_app/bot.py
#!/usr/bin/env bash
# exit on error
set -o errexit

# Устанавливаем только основные зависимости (без библиотек для тестов и разработки)
poetry install --only main --no-root

# Сбор статики
poetry run python manage.py collectstatic --no-input
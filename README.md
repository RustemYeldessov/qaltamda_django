# Qaltamda 💰

**Qaltamda** — это веб-приложение для управления личными финансами, написанное на Django. Проект помогает отслеживать расходы, классифицировать их по категориям и анализировать свои траты.

🚀 **Демо:** [expenzo-94dq.onrender.com](https://expenzo-94dq.onrender.com/)

---

## 🛠 Технологии
* **Backend:** Python 3.x, Django 5.x
* **API:** Django REST Framework (DRF)
* **Database:** PostgreSQL (на Render) / SQLite (локально)
* **Frontend:** Django Templates, CSS
* **Интеграции:** Telegram Bot

---

## ✨ Основные функции
- [x] **Управление расходами:** создание, редактирование и удаление записей.
- [x] **Категории и разделы:** гибкая структура трат.
- [x] **Личный кабинет:** каждый пользователь видит только свои данные.
- [x] **REST API:** эндпоинты для интеграции с внешними сервисами.
- [ ] **Telegram Bot:** быстрое добавление расходов через мессенджер (в процессе).
- [ ] **Аналитика:** графики и отчеты за месяц (в планах).

---

## 🚀 Локальный запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/RustemYeldessov/expenzo.git](https://github.com/RustemYeldessov/tengecash.git)
   cd tengecash

2. **Создайте виртуальное окружение:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Linux/macOS
    # или
    venv\Scripts\activate     # Для Windows
   
3. **Установите зависимости:**
    ```bash
   pip install -r requirements.txt

4. **Выполните миграции:**
    ```bash
   python manage.py migrate

5. **Запустите сервер:**
    ```bash
   python manage.py runserver
from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db import connections
from django.db.models import Sum

from qaltamda.users.models import User
from qaltamda.categories.models import Category
from qaltamda.sections.models import Section
from qaltamda.expenses.models import Expense

def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()


@sync_to_async
def registration_user_db(tg_id, username, first_name, last_name, password):
    if User.objects.filter(username=username).exists():
        return False, "Пользователь с таким логином уже существует."

    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            telegram_id=tg_id
        )
        return True, f"Получилось! Пользователь {username} успешно зарегистрирован!"
    except Exception as e:
        return False, f"Ошибка при регистрации: {str(e)}"


@sync_to_async
def logout_user_db(tg_id):
    user = User.objects.filter(telegram_id=tg_id).first()
    if user:
        user.telegram_id = None
        user.save()
        return True
    return False

@sync_to_async
def get_user_by_tg_id(tg_id):
    close_old_connections()
    return User.objects.filter(telegram_id=tg_id).first()

@sync_to_async
def bind_user_with_password(tg_id, django_username, password):
    user = authenticate(username=django_username, password=password)
    if user is not None:
        user.telegram_id = tg_id
        user.save()
        return f"Получилось! Ты вошел как пользователь {django_username}!"
    return "Ошибка: Пользователь с таким именем не найден в базе данных"

@sync_to_async
def logout_user_db(tg_id):
    user = User.objects.filter(telegram_id=tg_id).first()
    if user:
        user.telegram_id = None
        user.save()
        return True
    return False

@sync_to_async
def get_categories_db(user):
    return list(Category.objects.filter(user=user))

@sync_to_async
def update_category_name(cat_id, new_name):
    Category.objects.filter(id=cat_id).update(name=new_name)

@sync_to_async
def category_exists(user, name):
    return Category.objects.filter(user=user, name__iexact=name).exists()

@sync_to_async
def create_category(user, name):
    return Category.objects.create(user=user, name=name)

@sync_to_async
def category_delete(user, cat_id):
    return Category.objects.filter(id=cat_id, user=user).delete()

@sync_to_async
def get_first_section(user):
    return Section.objects.filter(user=user).first()

@sync_to_async
def create_expense(user, category_id, amount, description, section):
    category = Category.objects.get(id=category_id)
    return Expense.objects.create(
        user=user,
        category=category,
        section=section,
        amount=amount,
        description=description,
        date=timezone.now()
    )

@sync_to_async
def expense_exists(user, expense_id):
    return Expense.objects.filter(id=expense_id, user=user).exists()

@sync_to_async
def delete_expense_by_id(user, expense_id):
    return Expense.objects.filter(id=expense_id, user=user).delete()


@sync_to_async
def get_monthly_stats(user):
    today = timezone.now().date()
    start_date = today.replace(day=1)

    user_expenses = Expense.objects.filter(user=user)

    expenses_by_category = list(
        user_expenses.filter(date__gte=start_date, date__lte=today)
        .values("category__name")
        .annotate(sum=Sum("amount"))
        .order_by("-sum")
    )

    total_sum = sum(item['sum'] for item in expenses_by_category)

    return expenses_by_category, total_sum

@sync_to_async
def get_favorite_categories_db(user):
    favorites = list(Category.objects.filter(user=user, is_favorite=True))
    if not favorites:
        return list(Category.objects.filter(user=user))
    return favorites
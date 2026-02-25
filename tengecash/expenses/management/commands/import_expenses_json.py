import json
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from tengecash.categories.models import Category
from tengecash.expenses.models import Expense
from tengecash.sections.models import Section


class Command(BaseCommand):
    help = 'Импорт расходов из JSON файла'

    def handle(self, *args, **options):
        User = get_user_model()
        target_username = 'miumiu'
        user = User.objects.filter(username=target_username).first()

        if not user:
            self.stdout.write(self.style.ERROR(f'Пользователь {target_username} не найден!'))
            return

        file_path = 'expenses.json'

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            expenses_to_create = []  # Список для накопления объектов

            # Предварительно загружаем категории и разделы в память, чтобы не дергать базу постоянно
            # (Если их очень много, это сэкономит кучу времени)
            sections_cache = {s.name: s for s in Section.objects.all()}
            categories_cache = {c.name: c for c in Category.objects.filter(user=user)}

            for row in data:
                # Фильтруем только Рустема
                if row.get('Name', '').strip() != 'Ильмира':
                    continue

                if not row.get('Amount') or not row.get('Date'):
                    continue

                # Получаем/создаем раздел (с кэшированием)
                section_name = row['Section'].strip()
                if section_name not in sections_cache:
                    section, _ = Section.objects.get_or_create(name=section_name)
                    sections_cache[section_name] = section
                section = sections_cache[section_name]

                # Получаем/создаем категорию (с кэшированием)
                cat_name = row['Category'].strip()
                if cat_name not in categories_cache:
                    category, _ = Category.objects.get_or_create(name=cat_name, user=user)
                    categories_cache[cat_name] = category
                category = categories_cache[cat_name]

                # Подготовка суммы
                raw_amount = str(row['Amount'])
                clean_amount = raw_amount.replace(' ', '').replace('\xa0', '').replace(',', '.')
                final_amount = int(float(clean_amount))

                # Вместо .create() просто создаем объект в памяти
                expenses_to_create.append(Expense(
                    user=user,
                    section=section,
                    category=category,
                    date=datetime.strptime(row['Date'].strip(), '%Y-%m-%d').date(),
                    description=row['Description'].strip(),
                    amount=final_amount
                ))

            # ОДИН запрос в базу вместо 4000!
            Expense.objects.bulk_create(expenses_to_create, batch_size=500)

            self.stdout.write(self.style.SUCCESS(f'Успешно импортировано: {len(expenses_to_create)}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Критическая ошибка: {e}'))
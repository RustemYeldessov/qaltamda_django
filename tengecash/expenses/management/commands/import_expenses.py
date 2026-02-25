import csv
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from tengecash.categories.models import Category
from tengecash.expenses.models import Expense
from tengecash.sections.models import Section


class Command(BaseCommand):
    help = 'Импорт расходов из очищенного CSV'

    def handle(self, *args, **options):
        User = get_user_model()
        # 1. Исправляем получение юзера (добавили скобки)
        user = User.objects.filter(username='miumiu').first() or User.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR('Пользователь не найден!'))
            return

        file_path = 'new_expenses.csv'
        count = 0
        skipped_count = 0

        try:
            with open(file_path, encoding='utf-8-sig') as f:  # utf-8-sig лечит проблему с невидимыми символами
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        # Фильтрация по имени
                        if row.get('Name', '').strip() != 'Ильмира':
                            skipped_count += 1
                            continue

                        # Пропускаем пустые строки
                        if not row.get('Amount') or not row.get('Date'):
                            continue

                        # 1. Получаем/создаем Раздел
                        section, _ = Section.objects.get_or_create(
                            name=row['Section'].strip(),
                            user=user
                        )
                        # 2. Получаем/создаем Категорию
                        category, _ = Category.objects.get_or_create(
                            name=row['Category'].strip(),
                            user=user
                        )

                        # 3. Сумма (теперь через float, чтобы не упасть на "10.5")
                        clean_amount = row['Amount'].replace(' ', '').replace('\xa0', '').replace(',', '.')
                        final_amount = int(float(clean_amount))

                        # 4. Создаем запись
                        Expense.objects.create(
                            user=user,
                            section=section,
                            category=category,
                            date=datetime.strptime(row['Date'].strip(), '%Y-%m-%d').date(),
                            description=row['Description'].strip(),
                            amount=final_amount
                        )
                        count += 1

                    except Exception as line_error:
                        self.stdout.write(
                            self.style.WARNING(f"Ошибка в строке {count + skipped_count + 1}: {line_error}"))
                        continue

            self.stdout.write(self.style.SUCCESS(
                f'Импорт завершен!\n'
                f'Добавлено: {count}\n'
                f'Пропущено: {skipped_count}'
            ))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Файл {file_path} не найден.'))
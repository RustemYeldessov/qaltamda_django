import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from qaltamda.expenses.models import Expense
from qaltamda.categories.models import Category
from qaltamda.sections.models import Section

User = get_user_model()


@pytest.mark.django_db
class TestExpenseCRUD:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser1', password='test_pass123')

    @pytest.fixture
    def logged_client(self, client, user):
        client.login(username='testuser1', password='test_pass123')
        return client

    @pytest.fixture
    def category(self, user):
        return Category.objects.create(name='TestCategory', user=user)

    @pytest.fixture
    def section(self, user):
        return Section.objects.create(name='TestSection', user=user)

    @pytest.fixture
    def expense(self, user, section, category):
        return Expense.objects.create(
            amount=1000,
            category=category,
            section=section,
            user=user,
            description='Test Expense 1'
        )

    def test_expenses_list(self, logged_client, user, category, section):
        url = reverse('expenses:index')
        response = logged_client.get(url)
        assert response.status_code == 200
        assert 'Expenses' in response.content.decode()

    def test_expense_create(self, logged_client, user, category, section):
        url = reverse('expenses:create')
        data = {
            'amount': 1000,
            'category': category.id,
            'section': section.id,
            'description': 'Test Expense 2'
        }
        response = logged_client.post(url, data)

        assert response.status_code == 302
        assert Expense.objects.count() == 1
        new_expense = Expense.objects.first()
        assert new_expense.description == 'Test Expense 2'
        assert int(new_expense.amount) == 1000

    def test_expense_show(self, logged_client, expense):
        url = reverse('expenses:show', args=[expense.id])
        response = logged_client.get(url)
        assert response.status_code == 200
        templates = [t.name for t in response.templates if t.name]
        assert 'expenses/show.html' in templates

    def test_expense_update(self, logged_client, user, category, section, expense):
        url = reverse('expenses:update', args=[expense.id])
        data = {
            'amount': 2000,
            'category': category.id,
            'section': section.id,
            'user': user,
            'description': 'Test Expense Updated',
            'date': '2025-12-31'
        }
        response = logged_client.post(url, data)
        expense.refresh_from_db()
        assert response.status_code == 302
        assert expense.description == 'Test Expense Updated'
        assert int(expense.amount) == 2000

    def test_expense_delete(self, logged_client, expense):
        url = reverse('expenses:delete', args=[expense.id])
        response = logged_client.post(url)
        assert response.status_code == 302
        assert not Expense.objects.filter(id=expense.id).exists()

    def test_expense_delete_no_permission(self, client, expense):
        url = reverse('expenses:delete', args=[expense.id])
        response = client.post(url)
        assert response.status_code == 302
        assert Expense.objects.filter(id=expense.id).exists()
        assert response.url.startswith('/users/login/') or response.url == reverse('expenses:index')

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from qaltamda.categories.models import Category
from qaltamda.sections.models import Section
from qaltamda.expenses.models import Expense

User = get_user_model()


@pytest.mark.django_db
class TestAnalytics:

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
    def expense_1(self, user, section, category):
        return Expense.objects.create(
            amount=1000,
            category=category,
            section=section,
            user=user,
            description='Test Expense 1',
            date='2026-02-02'
        )

    @pytest.fixture
    def expense_2(self, user, section, category):
        return Expense.objects.create(
            amount=3000,
            category=category,
            section=section,
            user=user,
            description='Test Expense 2',
            date='2026-02-12'
        )

    @pytest.fixture
    def expense_3(self, user, section, category):
        return Expense.objects.create(
            amount=10000,
            category=category,
            section=section,
            user=user,
            description='Test Expense 3',
            date='2026-01-12'
        )

    def test_expenses_statistics_logic(self, logged_client, user, expense_1, expense_2, expense_3):
        url = reverse('analytics:statistics')
        response = logged_client.get(url)
        assert response.status_code == 200
        assert response.context['total_sum'] == 14000
        assert response.context['total_count'] == 3

    def test_filter_by_date(self, logged_client, user, expense_1, expense_2, expense_3):
        url = reverse('analytics:statistics')
        data = {
            'start_date': '2026-02-01',
            'end_date': '2026-02-25'
        }
        response = logged_client.get(url, data)
        assert response.status_code == 200
        assert response.context['total_sum_by_period'] == 4000

    def test_statistics_reset(self, logged_client):
        url = reverse('analytics:statistics')
        logged_client.get(url, {'start_date': '2026-01-01'})
        response = logged_client.get(url, {'reset': '1'})
        assert response.status_code == 302
        assert response.url == url

    def test_statistics_by_categories(self, logged_client, section, user):
        cat1 = Category.objects.create(name='Category 1', user=user)
        cat2 = Category.objects.create(name='Category 2', user=user)

        Expense.objects.create(
            amount=2000,
            category=cat1,
            section=section,
            user=user,
            description='Test expense 1'
        )
        Expense.objects.create(
            amount=1000,
            category=cat1,
            section=section,
            user=user,
            description='Test expense 2'
        )
        Expense.objects.create(
            amount=5000,
            category=cat2,
            section=section,
            user=user,
            description='Test expense 3'
        )
        url = reverse('analytics:statistics')
        response = logged_client.get(url)
        results = response.context['expenses_by_category']

        assert response.status_code == 200
        assert len(results) == 2

        assert results[0]['category__name'] == 'Category 2'
        assert results[0]['sum'] == 5000

        assert results[1]['category__name'] == 'Category 1'
        assert results[1]['sum'] == 3000

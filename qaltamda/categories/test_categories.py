import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from qaltamda.categories.models import Category
from qaltamda.sections.models import Section
from qaltamda.expenses.models import Expense

User = get_user_model()


@pytest.mark.django_db
class TestCategoriesCRUD:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='password123')

    @pytest.fixture
    def section(self, user):
        return Section.objects.create(name='test_section', user=user)

    @pytest.fixture
    def category(self, user):
        return Category.objects.create(name='Bug', user=user)

    @pytest.fixture
    def logged_client(self, client, user):
        client.login(username='testuser', password='password123')
        return client

    def test_category_list(self, logged_client, category):
        url = reverse('categories:index')
        response = logged_client.get(url)
        assert response.status_code == 200
        assert 'Bug' in response.content.decode()

    def test_category_create(self, logged_client):
        url = reverse('categories:create')
        response = logged_client.post(url, {'name': 'Feature'})
        assert response.status_code == 302
        assert Category.objects.filter(name='Feature').exists()

    def test_category_update(self, logged_client, category):
        url = reverse('categories:update', args=[category.id])
        response = logged_client.post(url, {'name': 'UpdatedCategory'})
        category.refresh_from_db()
        assert response.status_code == 302
        assert category.name == 'UpdatedCategory'

    def test_delete_category(self, logged_client, category):
        url = reverse('categories:delete', args=[category.id])
        response = logged_client.post(url)
        assert response.status_code == 302
        assert not Category.objects.filter(id=category.id).exists()

    def test_cannot_delete_category_in_use(self, logged_client, category, section, user):
        Expense.objects.create(
            amount=100,
            category=category,
            section=section,
            user=user,
            description='Test'
        )
        url = reverse('categories:delete', args=[category.pk])
        response = logged_client.post(url)
        assert response.status_code == 302
        assert Category.objects.filter(pk=category.pk).exists()

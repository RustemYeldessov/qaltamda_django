import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from qaltamda.expenses.models import Expense
from qaltamda.sections.models import Section
from qaltamda.categories.models import Category

User = get_user_model()


@pytest.mark.django_db
class TestSectionsCRUD:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='password123')

    @pytest.fixture
    def category(self, user):
        return Category.objects.create(name='NewCategory', user=user)

    @pytest.fixture
    def section(self, user):
        return Section.objects.create(name='NewSection', user=user)

    @pytest.fixture
    def logged_client(self, client, user):
        client.login(username='testuser', password='password123')
        return client

    def test_section_list(self, logged_client, section):
        url = reverse('sections:index')
        response = logged_client.get(url)
        assert response.status_code == 200
        assert 'NewSection' in response.content.decode()

    def test_section_create(self, logged_client):
        url = reverse('sections:create')
        response = logged_client.post(url, {'name': 'Feature'})
        assert response.status_code == 302
        assert Section.objects.filter(name='Feature').exists()

    def test_section_update(self, logged_client, section):
        url = reverse('sections:update', args=[section.id])
        response = logged_client.post(url, {'name': 'UpdatedSection'})
        section.refresh_from_db()
        assert response.status_code == 302
        assert section.name == 'UpdatedSection'

    def test_section_delete(self, logged_client, section):
        url = reverse('sections:delete', args=[section.id])
        response = logged_client.post(url)
        assert response.status_code == 302
        assert not Section.objects.filter(id=section.id).exists()

    def test_cannot_delete_section_in_use(self, logged_client, section, category, user):
        Expense.objects.create(
            amount=100,
            user=user,
            category=category,
            section=section,
            description='test'
        )
        url = reverse('sections:delete', args=[section.pk])
        response = logged_client.post(url)
        assert response.status_code == 302
        assert Section.objects.filter(pk=section.pk).exists()

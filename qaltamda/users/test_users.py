import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_django.fixtures import client

User = get_user_model()


@pytest.mark.django_db
class TestUsersCRUD:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser1', password='password123')

    @pytest.fixture
    def logged_client(self, client, user):
        client.login(username='testuser1', password='password123')
        return client

    def test_user_list(self, client):
        url = reverse('users:index')
        response = client.get(url)
        assert response.status_code == 200
        templates = [t.name for t in response.templates if t.name]
        assert 'users/index.html' in templates

    def test_user_create(self, client):
        url = reverse('users:create')
        data = {
            'username': 'testuser2',
            'first_name': 'Name',
            'last_name': 'Surname',
            'password1': 'vdvl4446',
            'password2': 'vdvl4446'
        }
        response = client.post(url, data)

        if response.status_code == 200:
            print(response.context['form'].errors)

        assert response.status_code == 302
        assert User.objects.filter(username='testuser2').exists()

    def test_user_update(self, logged_client, user):
        url = reverse('users:update', kwargs={'pk': user.id})
        data = {
            'username': 'testuser1',
            'first_name': 'UpdatedName',
            'last_name': 'UpdatedSurname',
            'password1': 'vdvl4446',
            'password2': 'vdvl4446'
        }
        response = logged_client.post(url, data)
        user.refresh_from_db()
        assert response.status_code == 302
        assert user.first_name == 'UpdatedName'
        assert user.last_name == 'UpdatedSurname'

    def test_user_delete(self, logged_client, user):
        url = reverse('users:delete', kwargs={'pk': user.id})
        response = logged_client.post(url)
        assert response.status_code == 302
        assert not User.objects.filter(id=user.id).exists()

    def test_user_logout(self, logged_client, user):
        url_logout = reverse('users:logout')
        response = logged_client.post(url_logout)
        assert response.status_code == 302
        assert '_auth_user_id' not in logged_client.session


import pytest
from djoser.views import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_info():
    return {'username': 'Evgenii',
            'email': 'khristoforover@gmail.com',
            'password': '25111965q',
            }

@pytest.fixture
def user_token(client):
    user = User.objects.create_user(email='123@mail.ru', username='evgenii', password='rnhsdf2')
    token = Token.objects.create(user=user)
    return client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')


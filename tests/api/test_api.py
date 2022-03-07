import json
import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File


@pytest.mark.django_db
def test_user_registration(client, user_info):
    url = 'http://127.0.0.1:8000/api/v1/auth/users/'
    resp = client.post(url, data=user_info)
    print(resp, resp.status_code)
    assert resp.status_code == 201

@pytest.mark.django_db
def test_user_login(client, user_info):
    client.post('http://127.0.0.1:8000/api/v1/auth/users/', data=user_info)
    url = 'http://127.0.0.1:8000/auth/token/login/'
    resp = client.post(url, data=user_info)
    print(resp, resp.status_code)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_upload(client, user_token):
    file = open('file_storage/test_download')
    data = {
        'file': file
    }
    response = client.post('http://127.0.0.1:8000/api/v1/upload/', data=data, format='multipart')
    assert response.status_code == 201

@pytest.mark.django_db
def test_download(client, user_token):
    file = open('file_storage/test_upload')
    data = {
        'file': file
    }
    client.post('http://127.0.0.1:8000/api/v1/upload/', data=data, format='multipart')
    resp2 = client.get('http://127.0.0.1:8000/api/v1/download/')
    assert resp2.status_code == 200

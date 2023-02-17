import pytest


@pytest.fixture
@pytest.mark.django_db
def access_token(client, django_user_model):
    username = 'test_user_2'
    password = '123qwe'
    django_user_model.objects.create(username=username,
                                     password=password,
                                     role='moderator')

    response = client.post('/user/token/',
                           {"username": username, "password": password},
                           content_type='application/json')

    return response.data["access"]

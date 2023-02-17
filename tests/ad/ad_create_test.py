import pytest


@pytest.mark.django_db
def test_ad_create(client, access_token, user, category):
    data = {
        "name": "Тестовое объявление",
        "price": 420,
        "author": user.pk,
        "category": category.pk,
        "description": ""
    }

    expected_data = {
        "id": 1,
        "is_published": False,
        "name": "Тестовое объявление",
        "price": 420,
        "description": "",
        "image": None,
        "author": user.pk,
        "category": category.pk
    }

    response = client.post('/ad/', data, HTTP_AUTHORIZATION=f'Bearer {access_token}')
    assert response.status_code == 201
    assert response.data == expected_data

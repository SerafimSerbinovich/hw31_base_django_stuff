import pytest


@pytest.fixture
@pytest.mark.django_db
def access_token(client, django_user_model):
    pass
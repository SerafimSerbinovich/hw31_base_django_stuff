import pytest
from ads.serializers import AdDetailSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_detail(client, access_token):
    ad = AdFactory.create()

    response = client.get(f'/ad/{ad.pk}/', HTTP_AUTHORIZATION=f'Bearer {access_token}')
    assert response.status_code == 200
    assert AdDetailSerializer(ad).data

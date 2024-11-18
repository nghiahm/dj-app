import pytest
from accounts.factory import UserFactory, MerchantFactory
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_create_promotion(api_client):
    user = UserFactory()
    MerchantFactory(user=user)
    payload = dict(name="productname")
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.post("/api/v1/accounts/promotions/", payload)
    assert response.status_code == 201

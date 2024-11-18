import pytest
from accounts.factory import UserFactory, MerchantFactory
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_create_merchant(api_client):
    user = UserFactory()
    payload = dict(name="merchantname")
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.post("/api/v1/accounts/merchants/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_merchant_error_more_than_one_merchant_per_user(api_client):
    user = UserFactory()
    MerchantFactory(user=user)
    payload = dict(name="merchantname")
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.post("/api/v1/accounts/merchants/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_merchant_unauthorized(api_client):
    payload = dict(name="merchantname")
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.post("/api/v1/accounts/merchants/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_retrieve_merchant(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get("/api/v1/accounts/merchants/")
    assert response.status_code == 200
    assert response.data["name"] == merchant.name


@pytest.mark.django_db
def test_retrieve_merchant_error_when_merchant_not_exists(api_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get("/api/v1/accounts/merchants/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_retrieve_merchant_unauthorized(api_client):
    user = UserFactory()
    MerchantFactory(user=user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.get("/api/v1/accounts/merchants/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_merchant(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    new_merchant_name = "newmerchantname"
    payload = dict(
        name=new_merchant_name,
    )
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.patch("/api/v1/accounts/merchants/", payload)
    merchant.refresh_from_db()
    assert response.status_code == 200
    assert response.data["name"] == new_merchant_name
    assert merchant.name == new_merchant_name


@pytest.mark.django_db
def test_update_merchant_unauthorized(api_client):
    new_merchant_name = "newmerchantname"
    payload = dict(
        name=new_merchant_name,
    )
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.patch("/api/v1/accounts/merchants/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_merchant(api_client):
    user = UserFactory()
    MerchantFactory(user=user)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.delete("/api/v1/accounts/merchants/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_merchant_unauthorized(api_client):
    user = UserFactory()
    MerchantFactory(user=user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.delete("/api/v1/accounts/merchants/")
    assert response.status_code == 401

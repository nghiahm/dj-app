import pytest
from accounts.factory import (
    UserFactory,
    MerchantFactory,
    ServiceFactory,
    CategoryFactory,
    HashtagFactory,
    KeywordFactory,
)
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_create_service(api_client):
    user = UserFactory()
    MerchantFactory(user=user)
    categories = CategoryFactory.create_batch(3)
    hashtags = HashtagFactory.create_batch(3)
    keywords = KeywordFactory.create_batch(3)
    payload = dict(
        name="servicename",
        category_ids=[category.pk for category in categories],
        hashtag_ids=[hashtag.pk for hashtag in hashtags],
        keyword_ids=[keyword.pk for keyword in keywords],
    )
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.post("/api/v1/accounts/services/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_service_error_no_merchant_existt(api_client):
    user = UserFactory()
    payload = {}
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.post("/api/v1/accounts/services/", payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_product_unauthorized(api_client):
    user = UserFactory()
    MerchantFactory(user=user)
    payload = {}
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.post("/api/v1/accounts/services/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_list_product(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    services = ServiceFactory.create_batch(3, merchant=merchant)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get("/api/v1/accounts/services/")
    assert response.status_code == 200
    for service in services:
        assert {"id": service.pk, "name": service.name} in [
            {"id": item["id"], "name": item["name"]} for item in response.json()["results"]
        ]


@pytest.mark.django_db
def test_list_product_unauthorized(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    ServiceFactory.create_batch(3, merchant=merchant)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.get("/api/v1/accounts/services/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_retrieve_product(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    service = ServiceFactory(merchant=merchant)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get(f"/api/v1/accounts/services/{service.pk}/")
    assert response.status_code == 200
    assert response.data["name"] == service.name


@pytest.mark.django_db
def test_retrieve_product_unauthorized(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    service = ServiceFactory(merchant=merchant)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.get(f"/api/v1/accounts/services/{service.pk}/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_product(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    service = ServiceFactory(merchant=merchant)
    new_product_name = "newservicename"
    payload = dict(name=new_product_name)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.patch(f"/api/v1/accounts/services/{service.pk}/", payload)
    service.refresh_from_db()
    assert response.status_code == 200
    assert response.data["name"] == new_product_name
    assert service.name == new_product_name


@pytest.mark.django_db
def test_update_product_unauthorized(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    service = ServiceFactory(merchant=merchant)
    payload = {}
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.patch(f"/api/v1/accounts/services/{service.pk}/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_product(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    service = ServiceFactory(merchant=merchant)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.delete(f"/api/v1/accounts/services/{service.pk}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_product_unauthorized(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    service = ServiceFactory(merchant=merchant)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.delete(f"/api/v1/accounts/services/{service.pk}/")
    assert response.status_code == 401

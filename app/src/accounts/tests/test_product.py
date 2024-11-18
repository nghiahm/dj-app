import pytest
from accounts.factory import UserFactory, MerchantFactory, ProductFactory
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_create_product(api_client):
    user = UserFactory()
    MerchantFactory(user=user)
    payload = dict(name="productname")
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.post("/api/v1/accounts/products/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_product_error_no_merchant(api_client):
    user = UserFactory()
    payload = dict(name="productname")
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.post("/api/v1/accounts/products/", payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_product_unauthorized(api_client):
    user = UserFactory()
    MerchantFactory(user=user)
    payload = dict(name="productname")
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.post("/api/v1/accounts/products/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_list_product(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    products = ProductFactory.create_batch(3, merchant=merchant)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get("/api/v1/accounts/products/")
    assert response.status_code == 200
    for product in products:
        assert {"id": product.pk, "name": product.name} in [
            {"id": item["id"], "name": item["name"]} for item in response.json()
        ]


@pytest.mark.django_db
def test_list_product_unauthorized(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    ProductFactory.create_batch(3, merchant=merchant)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.get("/api/v1/accounts/products/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_retrieve_product(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    product = ProductFactory(merchant=merchant)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get(f"/api/v1/accounts/products/{product.pk}/")
    assert response.status_code == 200
    assert response.data["name"] == product.name


@pytest.mark.django_db
def test_retrieve_product_unauthorized(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    product = ProductFactory(merchant=merchant)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.get(f"/api/v1/accounts/products/{product.pk}/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_product(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    product = ProductFactory(merchant=merchant)
    new_product_name = "newproductname"
    payload = dict(name=new_product_name)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.patch(f"/api/v1/accounts/products/{product.pk}/", payload)
    product.refresh_from_db()
    assert response.status_code == 200
    assert response.data["name"] == new_product_name
    assert product.name == new_product_name


@pytest.mark.django_db
def test_update_product_unauthorized(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    product = ProductFactory(merchant=merchant)
    new_product_name = "newproductname"
    payload = dict(name=new_product_name)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.patch(f"/api/v1/accounts/products/{product.pk}/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_product(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    product = ProductFactory(merchant=merchant)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.delete(f"/api/v1/accounts/products/{product.pk}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_product_unauthorized(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    product = ProductFactory(merchant=merchant)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.delete(f"/api/v1/accounts/products/{product.pk}/")
    assert response.status_code == 401

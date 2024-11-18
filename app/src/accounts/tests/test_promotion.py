import pytest
from accounts.factory import UserFactory, MerchantFactory, ProductFactory, ServiceFactory, PromotionFactory
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_create_promotion(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    product = ProductFactory(merchant=merchant)
    payload = dict(name="promotionname", product=product.pk)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.post("/api/v1/accounts/promotions/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_promotion_without_product_and_service(api_client):
    user = UserFactory()
    payload = dict(
        name="promotionname",
    )
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.post("/api/v1/accounts/promotions/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_promotion_unauthorized(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    product = ProductFactory(merchant=merchant)
    payload = dict(name="promotionname", product=product.pk)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.post("/api/v1/accounts/promotions/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_list_promotion(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    service = ServiceFactory(merchant=merchant)
    promotions = PromotionFactory.create_batch(3, service=service)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get("/api/v1/accounts/promotions/")
    assert response.status_code == 200
    for promotion in promotions:
        assert {"id": promotion.pk, "name": promotion.name} in [
            {"id": item["id"], "name": item["name"]} for item in response.json()
        ]


@pytest.mark.django_db
def test_list_promotion_unauthorized(api_client):
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.get("/api/v1/accounts/promotions/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_retrieve_promotion(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    service = ServiceFactory(merchant=merchant)
    promotion = PromotionFactory(service=service)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get(f"/api/v1/accounts/promotions/{promotion.pk}/")
    assert response.status_code == 200
    assert response.data["name"] == promotion.name


@pytest.mark.django_db
def test_retrieve_promotion_unauthorized(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    service = ServiceFactory(merchant=merchant)
    promotion = PromotionFactory(service=service)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.get(f"/api/v1/accounts/promotions/{promotion.pk}/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_promotion(api_client):
    user = UserFactory()
    merchant = MerchantFactory(user=user)
    product = ProductFactory(merchant=merchant)
    promotion = PromotionFactory(product=product)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.delete(f"/api/v1/accounts/promotions/{promotion.pk}/")
    assert response.status_code == 204

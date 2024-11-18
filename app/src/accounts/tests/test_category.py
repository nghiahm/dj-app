import pytest
from accounts.factory import (
    UserFactory,
    CategoryFactory,
)
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_create_category(api_client):
    user = UserFactory()
    payload = dict(
        name="categoryname",
    )
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.post("/api/v1/accounts/categories/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_category_unauthorized(api_client):
    payload = {}
    response = api_client.post("/api/v1/accounts/categories/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_list_category(api_client):
    user = UserFactory()
    categories = CategoryFactory.create_batch(3)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get("/api/v1/accounts/categories/")
    assert response.status_code == 200
    for category in categories:
        assert {"id": category.pk, "name": category.name} in [
            {"id": item["id"], "name": item["name"]} for item in response.json()["results"]
        ]


@pytest.mark.django_db
def test_list_category_unauthorized(api_client):
    response = api_client.get("/api/v1/accounts/categories/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_retrieve_category(api_client):
    user = UserFactory()
    category = CategoryFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get(f"/api/v1/accounts/categories/{category.pk}/")
    assert response.status_code == 200
    assert response.data["name"] == category.name


@pytest.mark.django_db
def test_retrieve_category_unauthorized(api_client):
    category = CategoryFactory()
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.get(f"/api/v1/accounts/categories/{category.pk}/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_category(api_client):
    user = UserFactory()
    category = CategoryFactory()
    new_category_name = "newcategoryname"
    payload = dict(name=new_category_name)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.patch(f"/api/v1/accounts/categories/{category.pk}/", payload)
    category.refresh_from_db()
    assert response.status_code == 200
    assert response.data["name"] == new_category_name
    assert category.name == new_category_name


@pytest.mark.django_db
def test_update_category_unauthorized(api_client):
    category = CategoryFactory()
    payload = {}
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.patch(f"/api/v1/accounts/services/{category.pk}/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_category(api_client):
    user = UserFactory()
    category = CategoryFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.delete(f"/api/v1/accounts/categories/{category.pk}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_category_unauthorized(api_client):
    category = CategoryFactory()
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.delete(f"/api/v1/accounts/categories/{category.pk}/")
    assert response.status_code == 401

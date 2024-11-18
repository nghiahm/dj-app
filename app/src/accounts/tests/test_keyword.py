import pytest
from accounts.factory import (
    UserFactory,
    KeywordFactory,
)
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_create_keyword(api_client):
    user = UserFactory()
    payload = dict(
        name="categoryname",
    )
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.post("/api/v1/accounts/keywords/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_keyword_unauthorized(api_client):
    payload = {}
    response = api_client.post("/api/v1/accounts/keywords/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_list_keyword(api_client):
    user = UserFactory()
    keywords = KeywordFactory.create_batch(3)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get("/api/v1/accounts/keywords/")
    assert response.status_code == 200
    for keyword in keywords:
        assert {"id": keyword.pk, "name": keyword.name} in [
            {"id": item["id"], "name": item["name"]} for item in response.json()["results"]
        ]


@pytest.mark.django_db
def test_list_keyword_unauthorized(api_client):
    response = api_client.get("/api/v1/accounts/keywords/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_retrieve_keyword(api_client):
    user = UserFactory()
    keyword = KeywordFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get(f"/api/v1/accounts/keywords/{keyword.pk}/")
    assert response.status_code == 200
    assert response.data["name"] == keyword.name


@pytest.mark.django_db
def test_retrieve_keyword_unauthorized(api_client):
    keyword = KeywordFactory()
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.get(f"/api/v1/accounts/keywords/{keyword.pk}/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_keyword(api_client):
    user = UserFactory()
    keyword = KeywordFactory()
    new_keyword_name = "newkeywordname"
    payload = dict(name=new_keyword_name)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.patch(f"/api/v1/accounts/keywords/{keyword.pk}/", payload)
    keyword.refresh_from_db()
    assert response.status_code == 200
    assert response.data["name"] == new_keyword_name
    assert keyword.name == new_keyword_name


@pytest.mark.django_db
def test_update_keyword_unauthorized(api_client):
    keyword = KeywordFactory()
    payload = {}
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.patch(f"/api/v1/accounts/services/{keyword.pk}/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_keyword(api_client):
    user = UserFactory()
    keyword = KeywordFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.delete(f"/api/v1/accounts/keywords/{keyword.pk}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_keyword_unauthorized(api_client):
    keyword = KeywordFactory()
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.delete(f"/api/v1/accounts/keywords/{keyword.pk}/")
    assert response.status_code == 401

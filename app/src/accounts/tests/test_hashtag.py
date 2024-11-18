import pytest
from accounts.factory import (
    UserFactory,
    HashtagFactory,
)
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_create_hashtag(api_client):
    user = UserFactory()
    payload = dict(
        name="hashtagname",
    )
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.post("/api/v1/accounts/hashtags/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_hashtag_unauthorized(api_client):
    payload = {}
    response = api_client.post("/api/v1/accounts/hashtags/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_list_hashtag(api_client):
    user = UserFactory()
    hashtags = HashtagFactory.create_batch(3)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get("/api/v1/accounts/hashtags/")
    assert response.status_code == 200
    for hashtag in hashtags:
        assert {"id": hashtag.pk, "name": hashtag.name} in [
            {"id": item["id"], "name": item["name"]} for item in response.json()["results"]
        ]


@pytest.mark.django_db
def test_list_hashtag_unauthorized(api_client):
    response = api_client.get("/api/v1/accounts/hashtags/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_retrieve_hashtag(api_client):
    user = UserFactory()
    hashtag = HashtagFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get(f"/api/v1/accounts/hashtags/{hashtag.pk}/")
    assert response.status_code == 200
    assert response.data["name"] == hashtag.name


@pytest.mark.django_db
def test_retrieve_hashtag_unauthorized(api_client):
    hashtag = HashtagFactory()
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.get(f"/api/v1/accounts/hashtags/{hashtag.pk}/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_hashtag(api_client):
    user = UserFactory()
    hashtag = HashtagFactory()
    new_hashtag_name = "newhashtagname"
    payload = dict(name=new_hashtag_name)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.patch(f"/api/v1/accounts/hashtags/{hashtag.pk}/", payload)
    hashtag.refresh_from_db()
    assert response.status_code == 200
    assert response.data["name"] == new_hashtag_name
    assert hashtag.name == new_hashtag_name


@pytest.mark.django_db
def test_update_hashtag_unauthorized(api_client):
    hashtag = HashtagFactory()
    payload = {}
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.patch(f"/api/v1/accounts/services/{hashtag.pk}/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_hashtag(api_client):
    user = UserFactory()
    hashtag = HashtagFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.delete(f"/api/v1/accounts/hashtags/{hashtag.pk}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_hashtag_unauthorized(api_client):
    hashtag = HashtagFactory()
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.delete(f"/api/v1/accounts/hashtags/{hashtag.pk}/")
    assert response.status_code == 401

import pytest
from accounts.factory import UserFactory
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_create_user(api_client):
    payload = dict(
        email="test@example.com",
        password="Abcd@123",
        first_name="Aaa",
        last_name="Bbb",
    )

    response = api_client.post("/api/v1/accounts/signup/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_obtain_token(api_client):
    user = UserFactory()
    payload = dict(
        email=user.email,
        password="testpassword",
    )
    response = api_client.post("/api/v1/accounts/token/", payload)
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_obtain_token_with_wrong_email(api_client):
    payload = dict(
        email="testemail",
        password="testpassword",
    )
    response = api_client.post("/api/v1/accounts/token/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_obtain_token_with_wrong_password(api_client):
    user = UserFactory()
    payload = dict(
        email=user.email,
        password="testwrongpassword",
    )
    response = api_client.post("/api/v1/accounts/token/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_refresh_token(api_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    payload = dict(
        refresh=str(refresh),
    )
    response = api_client.post("/api/v1/accounts/token/refresh/", payload)
    assert response.status_code == 200


@pytest.mark.django_db
def test_refresh_token_with_invalid_refresh_token(api_client):
    payload = dict(
        refresh="testrefreshtoken",
    )
    response = api_client.post("/api/v1/accounts/token/refresh/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_blacklist_token(api_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    payload = dict(
        refresh=str(refresh),
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.post("/api/v1/accounts/token/blacklist/", payload)
    assert response.status_code == 200


@pytest.mark.django_db
def test_blacklist_token_with_invalid_refresh_token(api_client):
    payload = dict(
        refresh="testrefreshtoken",
    )
    response = api_client.post("/api/v1/accounts/token/blacklist/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_blacklist_token_unauthorized(api_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    payload = dict(
        refresh=str(refresh),
    )
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.post("/api/v1/accounts/token/blacklist/", payload)
    assert response.status_code == 401

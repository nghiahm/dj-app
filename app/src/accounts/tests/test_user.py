import pytest
from accounts.factory import UserFactory
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_retrieve_user_details(api_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.get("/api/v1/accounts/details/")
    assert response.status_code == 200
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_retrieve_user_details_unauthorized(api_client):
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.get("/api/v1/accounts/details/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_user_details(api_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    new_first_name = "newfirstname"
    payload = dict(
        first_name=new_first_name,
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.put("/api/v1/accounts/details/", payload)
    user.refresh_from_db()
    assert response.status_code == 200
    assert response.data["first_name"] == new_first_name
    assert user.first_name == new_first_name


@pytest.mark.django_db
def test_update_user_details_unauthorized(api_client):
    new_first_name = "newfirstname"
    payload = dict(
        first_name=new_first_name,
    )
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.put("/api/v1/accounts/details/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_user(api_client):
    user = UserFactory()
    payload = dict(
        current_password="testpassword",
    )
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.delete("/api/v1/accounts/delete/", payload)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_user_with_invalid_password(api_client):
    user = UserFactory()
    payload = dict(
        current_password="invalidtestpassword",
    )
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    response = api_client.delete("/api/v1/accounts/delete/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_user_unauthorized(api_client):
    payload = dict(
        current_password="testpassword",
    )
    api_client.credentials(HTTP_AUTHORIZATION="Bearer ")
    response = api_client.delete("/api/v1/accounts/delete/", payload)
    assert response.status_code == 401

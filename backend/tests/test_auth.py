import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_login_and_first_password_flow(user):
    client = APIClient()
    login = client.post("/api/login/", {"username": "beginner", "password": "TempPass!234"}, format="json")
    assert login.status_code == 200
    assert login.data["data"]["must_change_password"] is True
    token = login.data["data"]["token"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    assert client.get("/api/menu/").status_code == 403
    assert client.get("/api/profile/").status_code == 200

    changed = client.post(
        "/api/profile/password/",
        {"old_password": "TempPass!234", "new_password": "NewPass!2345", "confirm_password": "NewPass!2345"},
        format="json",
    )
    assert changed.status_code == 200
    assert client.get("/api/profile/").status_code == 401
    relogin = APIClient().post("/api/login/", {"username": "beginner", "password": "NewPass!2345"}, format="json")
    assert relogin.data["data"]["must_change_password"] is False


@pytest.mark.django_db
def test_wrong_password_and_disabled_account(user):
    client = APIClient()
    assert client.post("/api/login/", {"username": "beginner", "password": "bad"}, format="json").status_code == 401
    user.is_active = False
    user.save(update_fields=["is_active"])
    assert client.post("/api/login/", {"username": "beginner", "password": "TempPass!234"}, format="json").status_code == 403


@pytest.mark.django_db
def test_superuser_does_not_need_first_change():
    admin = User.objects.create_superuser("admin", "admin@example.com", "AdminPass!234")
    response = APIClient().post("/api/login/", {"username": "admin", "password": "AdminPass!234"}, format="json")
    assert response.status_code == 200
    assert response.data["data"]["must_change_password"] is False


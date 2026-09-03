import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_admin_creates_user_with_email_role_and_temporary_password(client, menu_data):
    admin = User.objects.create_superuser("root", "root@example.com", "AdminPass!234")
    client.force_login(admin)

    response = client.post(
        reverse("admin:auth_user_add"),
        {
            "username": "created_by_admin",
            "email": "created@example.com",
            "password1": "Temporary!234",
            "password2": "Temporary!234",
            "roles": [str(menu_data[2].pk)],
            "_save": "保存",
        },
    )

    assert response.status_code == 302
    created = User.objects.get(username="created_by_admin")
    assert created.email == "created@example.com"
    assert created.profile.email == "created@example.com"
    assert created.profile.must_change_password is True
    assert list(created.profile.roles.values_list("code", flat=True)) == ["default_user"]


@pytest.mark.django_db
def test_admin_rejects_duplicate_email_ignoring_case(client, menu_data):
    admin = User.objects.create_superuser("root", "root@example.com", "AdminPass!234")
    User.objects.create_user("existing", "Same@example.com", "Existing!234")
    client.force_login(admin)

    response = client.post(
        reverse("admin:auth_user_add"),
        {
            "username": "duplicate_email",
            "email": "same@example.com",
            "password1": "Temporary!234",
            "password2": "Temporary!234",
            "roles": [str(menu_data[2].pk)],
            "_save": "保存",
        },
    )

    assert response.status_code == 200
    assert "该邮箱已被使用" in response.content.decode()
    assert not User.objects.filter(username="duplicate_email").exists()


@pytest.mark.django_db
def test_one_click_admin_can_log_in_and_is_reset_on_repeat():
    call_command("setup_admin")
    admin = User.objects.get(username="admin")
    assert admin.is_superuser is True
    assert admin.is_staff is True
    assert admin.check_password("Admin@123456") is True
    assert APIClient().post("/api/login/", {"username": "admin", "password": "Admin@123456"}, format="json").status_code == 200

    admin.set_password("ChangedPassword!234")
    admin.save(update_fields=["password"])
    call_command("setup_admin")
    admin.refresh_from_db()
    assert admin.check_password("Admin@123456") is True

import io

import pytest
from PIL import Image
from rest_framework.test import APIClient


def authenticated_client(user):
    client = APIClient()
    response = client.post("/api/login/", {"username": user.username, "password": "TempPass!234"}, format="json")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['data']['token']}")
    return client


@pytest.mark.django_db
def test_profile_validation_and_update(user):
    client = authenticated_client(user)
    invalid = client.put("/api/profile/", {"phone": "123"}, format="json")
    assert invalid.status_code == 400
    updated = client.put("/api/profile/", {"nickname": "小明", "phone": "13800138000", "email": "new@example.com"}, format="json")
    assert updated.status_code == 200
    assert updated.data["data"]["nickname"] == "小明"


@pytest.mark.django_db
def test_menu_and_example_permission(user, menu_data):
    user.profile.must_change_password = False
    user.profile.save(update_fields=["must_change_password"])
    client = authenticated_client(user)
    menu = client.get("/api/menu/")
    assert [item["code"] for item in menu.data["data"]] == ["dashboard"]
    assert client.get("/api/example/").status_code == 403
    user.profile.roles.first().menus.add(menu_data[1])
    assert client.get("/api/example/").status_code == 200


@pytest.mark.django_db
def test_avatar_rejects_fake_file_and_accepts_image(user, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    client = authenticated_client(user)
    fake = io.BytesIO(b"not an image")
    fake.name = "fake.png"
    assert client.post("/api/profile/avatar/", {"avatar": fake}, format="multipart").status_code == 400

    image_file = io.BytesIO()
    Image.new("RGB", (500, 300), "blue").save(image_file, "PNG")
    image_file.seek(0)
    image_file.name = "avatar.png"
    uploaded = client.post("/api/profile/avatar/", {"avatar": image_file}, format="multipart")
    assert uploaded.status_code == 200
    user.profile.refresh_from_db()
    with Image.open(user.profile.avatar.path) as saved:
        assert saved.size == (320, 320)
        assert saved.format == "WEBP"
    assert client.delete("/api/profile/avatar/").status_code == 200


@pytest.mark.django_db
def test_avatar_rejects_oversized_file(user):
    client = authenticated_client(user)
    oversized = io.BytesIO(b"x" * (2 * 1024 * 1024 + 1))
    oversized.name = "large.png"
    response = client.post("/api/profile/avatar/", {"avatar": oversized}, format="multipart")
    assert response.status_code == 400
    assert response.data["msg"] == "头像不能超过 2MB"


@pytest.mark.django_db
def test_health_endpoint():
    response = APIClient().get("/api/health/")
    assert response.status_code == 200
    assert response.data["data"]["database"] == "ok"

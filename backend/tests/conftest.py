import os

os.environ.setdefault("DJANGO_USE_SQLITE", "true")

import pytest
from django.contrib.auth.models import User

from permission.models import Menu, Role


@pytest.fixture
def menu_data(db):
    dashboard = Menu.objects.create(code="dashboard", name="首页", path="/index/dashboard", sort=1)
    example = Menu.objects.create(code="example", name="权限示例", path="/index/example", sort=2)
    role = Role.objects.create(code="default_user", name="普通用户")
    role.menus.add(dashboard)
    return dashboard, example, role


@pytest.fixture
def user(db, menu_data):
    user = User.objects.create_user("beginner", "beginner@example.com", "TempPass!234")
    user.profile.roles.add(menu_data[2])
    return user


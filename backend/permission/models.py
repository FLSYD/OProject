import uuid

from django.contrib.auth.models import User
from django.db import models


def avatar_upload_to(instance, filename):
    return f"avatars/{instance.user_id}/{uuid.uuid4().hex}.webp"


class Menu(models.Model):
    code = models.SlugField("菜单编码", max_length=50, unique=True)
    name = models.CharField("菜单名称", max_length=50)
    path = models.CharField("前端路由", max_length=100)
    icon = models.CharField("图标", max_length=50, blank=True)
    sort = models.PositiveIntegerField("排序", default=1)
    enabled = models.BooleanField("启用", default=True)

    class Meta:
        ordering = ["sort", "id"]
        verbose_name = "菜单"
        verbose_name_plural = "菜单"

    def __str__(self):
        return self.name


class Role(models.Model):
    code = models.SlugField("角色编码", max_length=50, unique=True)
    name = models.CharField("角色名称", max_length=50)
    description = models.CharField("说明", max_length=200, blank=True)
    enabled = models.BooleanField("启用", default=True)
    menus = models.ManyToManyField(Menu, blank=True, related_name="roles", verbose_name="菜单")

    class Meta:
        ordering = ["id"]
        verbose_name = "角色"
        verbose_name_plural = "角色"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "男"
        FEMALE = "female", "女"
        PRIVATE = "private", "保密"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="用户")
    roles = models.ManyToManyField(Role, blank=True, related_name="users", verbose_name="角色")
    nickname = models.CharField("昵称", max_length=50, blank=True)
    email = models.EmailField("邮箱", blank=True)
    phone = models.CharField("手机号", max_length=11, blank=True)
    gender = models.CharField("性别", max_length=10, choices=Gender.choices, blank=True)
    birthday = models.DateField("生日", blank=True, null=True)
    address = models.CharField("地址", max_length=200, blank=True)
    bio = models.CharField("个人简介", max_length=200, blank=True)
    avatar = models.ImageField("头像", upload_to=avatar_upload_to, blank=True)
    must_change_password = models.BooleanField("首次登录必须修改密码", default=True)
    token_version = models.PositiveIntegerField("令牌版本", default=1)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"

    def __str__(self):
        return self.nickname or self.user.username


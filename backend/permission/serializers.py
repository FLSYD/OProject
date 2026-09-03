import re

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Menu, UserProfile


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["code", "name", "path", "icon", "sort"]


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    roles = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "username", "nickname", "email", "phone", "gender", "birthday",
            "address", "bio", "avatar", "roles", "must_change_password",
            "created_at", "updated_at",
        ]
        read_only_fields = ["must_change_password", "created_at", "updated_at"]

    def get_roles(self, obj):
        if obj.user.is_superuser:
            return ["超级管理员"]
        return list(obj.roles.filter(enabled=True).values_list("name", flat=True))

    def get_avatar(self, obj):
        if not obj.avatar:
            return ""
        request = self.context.get("request")
        return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url

    def validate_phone(self, value):
        if value and not re.fullmatch(r"1[3-9]\d{9}", value):
            raise serializers.ValidationError("请输入正确的中国大陆手机号")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email__iexact=value).exclude(pk=self.instance.user_id).exists():
            raise serializers.ValidationError("该邮箱已被使用")
        return value

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.user.email = instance.email
        instance.user.save(update_fields=["email"])
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"old_password": ["原密码错误"]})
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": ["两次输入的新密码不一致"]})
        from django.contrib.auth.password_validation import validate_password

        validate_password(attrs["new_password"], user=user)
        return attrs

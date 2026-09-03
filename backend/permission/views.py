import io

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import connection, transaction
from PIL import Image, ImageOps, UnidentifiedImageError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Menu
from .permissions import PasswordReadyPermission, RequiredMenuPermission
from .responses import error, success
from .serializers import ChangePasswordSerializer, MenuSerializer, ProfileSerializer


def issue_access_token(user):
    token = RefreshToken.for_user(user).access_token
    token["token_version"] = user.profile.token_version
    return str(token)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = str(request.data.get("username", "")).strip()
        password = str(request.data.get("password", ""))
        existing = User.objects.filter(username=username).first()
        if existing and not existing.is_active:
            return error("账号已被禁用", 403)
        user = authenticate(request, username=username, password=password)
        if user is None:
            return error("用户名或密码错误", 401)
        profile = user.profile
        return success(
            {
                "token": issue_access_token(user),
                "user": ProfileSerializer(profile, context={"request": request}).data,
                "must_change_password": profile.must_change_password,
            },
            "登录成功",
        )


class MenuView(APIView):
    permission_classes = [PasswordReadyPermission]

    def get(self, request):
        if request.user.is_superuser:
            menus = Menu.objects.filter(enabled=True)
        else:
            menus = Menu.objects.filter(enabled=True, roles__enabled=True, roles__users=request.user.profile).distinct()
        return success(MenuSerializer(menus, many=True).data)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return success(ProfileSerializer(request.user.profile, context={"request": request}).data)

    def put(self, request):
        serializer = ProfileSerializer(request.user.profile, data=request.data, partial=True, context={"request": request})
        if not serializer.is_valid():
            return error("资料校验失败", 400, serializer.errors)
        serializer.save()
        return success(serializer.data, "资料保存成功")


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return error("密码修改失败", 400, serializer.errors)
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        profile = user.profile
        profile.must_change_password = False
        profile.token_version += 1
        profile.save(update_fields=["must_change_password", "token_version", "updated_at"])
        return success(None, "密码修改成功，请重新登录")


class AvatarView(APIView):
    permission_classes = [IsAuthenticated]
    allowed_formats = {"JPEG", "PNG", "WEBP"}

    def post(self, request):
        upload = request.FILES.get("avatar")
        if not upload:
            return error("请选择头像文件")
        if upload.size > 2 * 1024 * 1024:
            return error("头像不能超过 2MB")
        try:
            image = Image.open(upload)
            image.verify()
            upload.seek(0)
            image = Image.open(upload)
            if image.format not in self.allowed_formats:
                return error("仅支持 JPEG、PNG、WebP 图片")
            image = ImageOps.exif_transpose(image).convert("RGB")
            image = ImageOps.fit(image, (320, 320), Image.Resampling.LANCZOS)
        except (Image.DecompressionBombError, UnidentifiedImageError, OSError, ValueError):
            return error("文件不是有效图片")

        output = io.BytesIO()
        image.save(output, format="WEBP", quality=90)
        profile = request.user.profile
        old_name = profile.avatar.name if profile.avatar else ""
        profile.avatar.save("avatar.webp", ContentFile(output.getvalue()), save=True)
        if old_name and old_name != profile.avatar.name:
            profile.avatar.storage.delete(old_name)
        return success(ProfileSerializer(profile, context={"request": request}).data, "头像上传成功")

    def delete(self, request):
        profile = request.user.profile
        if profile.avatar:
            name = profile.avatar.name
            profile.avatar.delete(save=False)
            profile.avatar = ""
            profile.save(update_fields=["avatar", "updated_at"])
            if name and profile.avatar.storage.exists(name):
                profile.avatar.storage.delete(name)
        return success(None, "已恢复默认头像")


class ExampleView(APIView):
    permission_classes = [RequiredMenuPermission]
    required_menu_code = "example"

    def get(self, request):
        return success({"text": "这是一个受角色菜单保护的示例接口。"})


class HealthView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        except Exception:
            return error("数据库连接失败", 503)
        return success({"database": "ok"}, "服务正常")

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class VersionedJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        if not user.is_active:
            raise AuthenticationFailed("账号已被禁用")
        profile = user.profile
        if int(validated_token.get("token_version", 0)) != profile.token_version:
            raise AuthenticationFailed("登录状态已失效，请重新登录")
        return user


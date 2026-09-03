from rest_framework.permissions import BasePermission


class PasswordReadyPermission(BasePermission):
    message = "首次登录必须先修改初始密码"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_superuser or not request.user.profile.must_change_password))


class RequiredMenuPermission(PasswordReadyPermission):
    message = "没有访问该功能的权限"

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            self.message = "首次登录必须先修改初始密码"
            return False
        if request.user.is_superuser:
            return True
        code = getattr(view, "required_menu_code", "")
        return request.user.profile.roles.filter(enabled=True, menus__enabled=True, menus__code=code).exists()


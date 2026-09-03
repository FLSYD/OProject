from django.core.management.base import BaseCommand

from permission.models import Menu, Role


class Command(BaseCommand):
    help = "初始化新手模板的角色和菜单"

    def handle(self, *args, **options):
        dashboard, _ = Menu.objects.update_or_create(
            code="dashboard",
            defaults={"name": "首页", "path": "/index/dashboard", "icon": "el-icon-s-home", "sort": 1, "enabled": True},
        )
        example, _ = Menu.objects.update_or_create(
            code="example",
            defaults={"name": "权限示例", "path": "/index/example", "icon": "el-icon-lock", "sort": 2, "enabled": True},
        )
        default_role, _ = Role.objects.update_or_create(
            code="default_user", defaults={"name": "普通用户", "description": "只能访问公共首页", "enabled": True}
        )
        default_role.menus.set([dashboard])
        admin_role, _ = Role.objects.update_or_create(
            code="system_admin", defaults={"name": "系统管理员", "description": "可访问全部教学菜单", "enabled": True}
        )
        admin_role.menus.set([dashboard, example])
        self.stdout.write(self.style.SUCCESS("角色和菜单初始化完成"))


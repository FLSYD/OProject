from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand

from permission.models import Role


class Command(BaseCommand):
    help = "创建浏览器测试账号（只用于本地 E2E）"

    def handle(self, *args, **options):
        call_command("init_system")
        admin, _ = User.objects.get_or_create(username="e2e_admin", defaults={"email": "e2e_admin@example.test", "is_staff": True, "is_superuser": True})
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True
        admin.set_password("E2E_Admin!234")
        admin.save()
        admin.profile.must_change_password = False
        admin.profile.save(update_fields=["must_change_password"])

        user, _ = User.objects.get_or_create(username="e2e_user", defaults={"email": "e2e_user@example.test"})
        user.is_active = True
        user.set_password("E2E_Temp!234")
        user.save()
        user.profile.must_change_password = True
        user.profile.roles.set([Role.objects.get(code="default_user")])
        user.profile.save(update_fields=["must_change_password"])
        self.stdout.write(self.style.SUCCESS("E2E 账号创建完成"))


from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "创建或重置一键启动专用管理员"

    username = "admin"
    password = "Admin@123456"
    email = "admin@example.com"

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username=self.username,
            defaults={"email": self.email, "is_staff": True, "is_superuser": True, "is_active": True},
        )
        if not created and not user.is_superuser:
            raise CommandError("用户名 admin 已存在但不是管理员，请在 Django Admin 中处理该账号。")
        user.email = self.email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(self.password)
        user.save(update_fields=["email", "is_staff", "is_superuser", "is_active", "password"])
        user.profile.must_change_password = False
        user.profile.save(update_fields=["must_change_password", "updated_at"])
        action = "创建" if created else "重置"
        self.stdout.write(self.style.SUCCESS(f"一键管理员已{action}：{self.username} / {self.password}"))

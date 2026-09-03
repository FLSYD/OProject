from django.apps import AppConfig


class PermissionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "permission"
    verbose_name = "账号与权限"

    def ready(self):
        from . import signals  # noqa: F401


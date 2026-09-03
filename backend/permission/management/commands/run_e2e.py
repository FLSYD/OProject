import os

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "使用 SQLite 启动独立 E2E 服务"

    def handle(self, *args, **options):
        os.environ["DJANGO_USE_SQLITE"] = "true"
        call_command("migrate", interactive=False, verbosity=0)
        call_command("seed_e2e")
        call_command("runserver", "127.0.0.1:18000", use_reloader=False)

#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")
    # E2E 命令在 Django 读取 settings.py 前切换到独立 SQLite。
    if len(sys.argv) > 1 and sys.argv[1] == "run_e2e":
        os.environ.setdefault("DJANGO_USE_SQLITE", "true")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

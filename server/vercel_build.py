"""Production-only migrations for the isolated demonstration database."""

import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.vercel")
django.setup()
if os.environ.get("VERCEL_ENV") == "production":
    call_command("migrate", interactive=False)
call_command("collectstatic", interactive=False)

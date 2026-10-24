"""Free demo: stateless HTTP functions, persistent Postgres, request-driven clock."""

import os

# Use only the platform-provided exact hostnames, never a wildcard domain.
production_host = os.environ.get("VERCEL_PROJECT_PRODUCTION_URL")
if production_host:
    os.environ.setdefault("FRONTEND_URL", f"https://{production_host}")
from .cloud import *  # noqa: E402,F403

if production_host and production_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(production_host)
    CSRF_TRUSTED_ORIGINS.append(f"https://{production_host}")
SIMULACAO_SOB_DEMANDA = True
# PostgreSQL transaction poolers cannot safely retain server-side cursors.
DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True

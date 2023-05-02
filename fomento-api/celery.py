import os

from celery import Celery

import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fomento-api.settings")
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(
    BROKER_URL=env("REDIS_URL"), CELERY_RESULT_BACKEND=env("REDIS_URL")
)
app.autodiscover_tasks()

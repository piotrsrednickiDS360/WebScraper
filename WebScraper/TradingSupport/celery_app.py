# celery_app.py
from __future__ import absolute_import
import os

import celery
from celery import Celery
# default django settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE','TradingSupport.settings')
app = Celery('TradingSupportApp')
app.conf.timezone = 'UTC'
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
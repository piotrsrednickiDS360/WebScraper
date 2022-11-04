from django.core.management.base import BaseCommand
import datetime
from TradingSupportApp.FunctionsForDataExtraction import scrap_data_announcements_and_assembly, \
    scrap_data_pointers, \
    scrap_data_names
from TradingSupportApp.models import Company, Pointers, Announcements, AssemblyAnnouncements
import os
import django

from TradingSupportApp.tasks import scrap


class Command(BaseCommand):
    def handle(self, **options):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TradingSupport.settings")
        django.setup()
        scrap()



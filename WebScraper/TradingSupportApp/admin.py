from django.contrib import admin
from .models import Company, Announcements, Pointers
# Register your models here.

admin.site.register(Company)
admin.site.register(Announcements)
admin.site.register(Pointers)

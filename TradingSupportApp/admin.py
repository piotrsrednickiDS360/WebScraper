from django.contrib import admin
from .models import Company, Announcements, Pointers, AssemblyAnnouncements


# Register your models here.
class AnnouncementsAdmin(admin.ModelAdmin):
    """
        Class builds the admin model for class Announcements
        Arguments:
    """
    list_filter = [
        "company",
        "text",
        "date",
    ]
    list_display = ("company", "text", "date",)
    ordering = ("company",)


admin.site.register(Announcements, AnnouncementsAdmin)


class PointersAdmin(admin.ModelAdmin):
    """
            Class builds the admin model for class Pointers
            Arguments:
    """
    list_filter = [
        "company",
        "name",
        "value",
    ]
    list_display = ("company", "name", "value",)
    ordering = ("company",)


admin.site.register(Pointers, PointersAdmin)


class AssemblyAnnouncementsAdmin(admin.ModelAdmin):
    """
            Class builds the admin model for class AssemblyAnnouncements
            Arguments:
    """
    list_filter = [
        "company",
        "text",
        "date",
    ]
    list_display = ("company", "text", "date",)
    ordering = ("company",)


admin.site.register(AssemblyAnnouncements, AssemblyAnnouncementsAdmin)


class CompanyAdmin(admin.ModelAdmin):
    """
            Class builds the admin model for class Announcements
            Arguments:
    """
    list_filter = [
        "symbol",
    ]
    list_display = ('symbol',)
    ordering = ('symbol',)


admin.site.register(Company, CompanyAdmin)

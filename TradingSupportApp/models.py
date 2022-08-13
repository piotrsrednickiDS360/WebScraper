from django.db import models
import datetime


class Company(models.Model):
    symbol = models.CharField(max_length=10)
    wanted = models.BooleanField(default=True)


class UnwantedCompanies(models.Model):
    symbol = models.CharField(max_length=10)
    wanted = models.BooleanField(default=False)
    user = models.CharField(max_length=30)


class Indexes(models.Model):
    name = models.CharField(max_length=10)
    value = models.CharField(max_length=10)


class Pointers(models.Model):
    name = models.CharField(max_length=10)
    value = models.CharField(max_length=10)


class Announcements(models.Model):
    date = models.DateField()
    text = models.CharField(max_length=10)

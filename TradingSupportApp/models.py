from django.db import models
import datetime


class Company(models.Model):
    symbol = models.CharField(max_length=10)
    wanted = models.BooleanField(default=True)
    name = models.CharField(max_length=150)


class UnwantedCompanies(models.Model):
    symbol = models.CharField(max_length=10)
    wanted = models.BooleanField(default=False)
    name = models.CharField(max_length=150)
    user = models.CharField(max_length=30)


class Pointers(models.Model):
    name = models.CharField(max_length=10)
    value = models.CharField(max_length=10)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Announcements(models.Model):
    date = models.DateField()
    text = models.CharField(max_length=10)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)


class Assemblies(models.Model):
    date = models.DateField()
    text = models.CharField(max_length=10)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)

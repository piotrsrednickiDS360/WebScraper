from django.db import models
import datetime


class Company(models.Model):
    """
        Class represents a company from bankier.pl
        Arguments:
    """
    symbol = models.CharField(max_length=10)
    wanted = models.BooleanField(default=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.symbol


class UnwantedCompanies(models.Model):
    """
        Class represents an unwanted Company object
        Arguments:
    """
    symbol = models.CharField(max_length=10)
    wanted = models.BooleanField(default=False)
    name = models.CharField(max_length=150)
    user = models.CharField(max_length=30)

    def __str__(self):
        return self.symbol


class Pointers(models.Model):
    """
        Class represents pointers of a company from bankier.pl
        Arguments:
    """
    name = models.CharField(max_length=10)
    value = models.CharField(max_length=10)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Announcements(models.Model):
    """
        Class represents an announncement of a company from bankier.pl
        Arguments:
    """
    date = models.DateField()
    text = models.CharField(max_length=10)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)


class AssemblyAnnouncements(models.Model):
    """
        Class represents an assembly announcement of a company from bankier.pl
        Arguments:
    """
    date = models.DateField()
    text = models.CharField(max_length=10)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)

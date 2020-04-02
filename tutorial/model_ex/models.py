from django.db import models
import datetime


class Company(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=20, default='0000000')
    date_created = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=20)
    creator = models.CharField(max_length=20, default='0000000')
    date_created = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.name

class Programmer(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    langages = models.ManyToManyField(Language)

    def __str__(self):
        return self.name





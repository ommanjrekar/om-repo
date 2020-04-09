# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Employee(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    doj = models.CharField(max_length=20)
    edu = models.CharField(max_length=20)
    loc = models.CharField(max_length=20)

    class Meta:
        app_label = 'dashboard'
        db_table = 'employee'

    def __str__(self):
        return self.name
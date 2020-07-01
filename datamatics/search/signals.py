from .models import Employee
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Employee)
def index_emp(sender, instance, **kwargs):
    instance.indexing()

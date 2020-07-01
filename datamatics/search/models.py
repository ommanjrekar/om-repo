from django.db import models
from .search import EmpIndex


class Employee(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def indexing(self):
        obj = EmpIndex(
            meta={'id':self.id},
            name=self.name,
            code=self.code,
            location=self.location
        )
        obj.save()
        return obj.to_dict(include_meta=True)
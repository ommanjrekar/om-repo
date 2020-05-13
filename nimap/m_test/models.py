from django.db import models
from datetime import datetime

class User(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name




class Project(models.Model):
    project_name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name


class Client(models.Model):
    client_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.client_name

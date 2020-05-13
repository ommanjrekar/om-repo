from django.contrib import admin
from .models import User, Client, Project


admin.site.register(User)
admin.site.register(Client)
admin.site.register(Project)


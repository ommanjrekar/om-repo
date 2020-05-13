from .models import User, Client, Project
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']


    
class ProjectSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True, read_only=True) 
    class Meta:
        model = Project
        fields = '__all__'        

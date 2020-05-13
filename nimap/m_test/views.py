from django.shortcuts import render
from rest_framework import generics
from .models import User, Client, Project
from .serializers import UserSerializer, ClientSerializer, ProjectSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated  


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]



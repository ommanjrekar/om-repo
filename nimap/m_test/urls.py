from django.urls import path
from m_test import views


urlpatterns = [
    path('user/', views.UserList.as_view()),
    path('user/<int:pk>', views.UserDetailView.as_view()),
    path('client/', views.ClientList.as_view()),
    path('client/<int:pk>', views.ClientDetailView.as_view()),
    path('project/', views.ProjectList.as_view()),
    path('project/<int:pk>', views.ProjectDetailView.as_view()),
]
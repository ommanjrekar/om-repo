from django.urls import path, include
from . import views
#from rest_framework.routers import DefaultRouter


#router = DefaultRouter()
#router.register('api/puppy', views.PuppyViewset)
urlpatterns = [
#    path('', include(router.urls)),
    path('puppies/', views.Puppy_list.as_view()),
    path('puppies/<int:pk>', views.PuppyDetail.as_view())
]
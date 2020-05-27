from rest_framework.routers import DefaultRouter
from django.urls import path, include

from rcp import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ing', views.IngredientViewset)
router.register('rcp', views.RecipeViewset)
app_name='rcp'

urlpatterns = [
    path('', include(router.urls)),
]
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TagSerializers, IngredientSerializer, RecipeSerializer, RecipeDetailSerializer
from core.models import Tag, Ingredient, Recipe



class RcpAttrs(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base class for Tag and Ingredien classes which has common code"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return objects for the current logged in user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create new tag"""
        serializer.save(user=self.request.user)


class TagViewSet(RcpAttrs):
    """Manage tags in db"""
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializers


class IngredientViewset(RcpAttrs):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer



class RecipeViewset(viewsets.ModelViewSet):
    """Manage recipe db"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Terurn appropriate serializer class"""
        if self.action == 'retrieve':
            return RecipeDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create new recipe """
        serializer.save(user=self.request.user)


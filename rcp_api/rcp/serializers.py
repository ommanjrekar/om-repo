from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id', )


class IngredientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):

    ingredient = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minutes', 'ingredient', 'tags', 'price', 'link')
        read_only_fields = ('id', )


class RecipeDetailSerializer(RecipeSerializer):
    """Detail serializer"""
    ingredient = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializers(many=True, read_only=True)
from django.contrib.auth.models import User
from rest_framework import serializers

from recipedb.models import Recipe, Ingredient, UNITS, RecipeIngredient
class UnitSerializer(serializers.Serializer):
    abbr = serializers.CharField()
    name = serializers.CharField()

class RecipeIngredientSerializer(serializers.ModelSerializer):
    unit = serializers.ChoiceField(choices=UNITS)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'created', 'recipe', 'ingredient', 'amount', 'unit')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'created',
            'name',
            'description',
            'image',
            'steps',
            'ingredients'
        )

    def create(self, validated_data):
        """
        Create and return a new `Recipe` instance, given the validated data.
        :return: A new Recipe instance
        """
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            ingredient_data['recipe'] = recipe
            RecipeIngredient.objects.create(**ingredient_data)
        return recipe

    def update(self, instance, validated_data):
        """
        Update and return an existing `Recipe` instance, given the validated data.
        :param instance:
        :param validated_data:
        :return:
        """
        ingredients_data = validated_data.pop('ingredients')

        ingredients = RecipeIngredient.objects.filter(recipe=instance.id)

        not_in_list = lambda ingredient, list: not [y for y in ingredients_data
                                                        if ingredient.ingredient == y["ingredient"]]

        for ingredient in [x for x in list(ingredients) if not_in_list(x, ingredients)]:
            ingredient.delete()


        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.update_or_create(**ingredient_data)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.steps = validated_data.get('steps', instance.steps)
        instance.save()
        return instance


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'created',
            'name',
            'description',
            'image',
            'estprice',
        )

class UserSerializer(serializers.ModelSerializer):
    #recipes = serializers.PrimaryKeyRelatedField(many=True, queryset=Recipe.objects.all())

    class Meta:
        model = User
        fields = (
            'id',
            'username',
        #    'recipes',
        )
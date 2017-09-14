from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route

from recipedb.models import Recipe, Ingredient, RecipeIngredient
from recipedb.serializers import RecipeSerializer, IngredientSerializer, RecipeIngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    queryset = Recipe.objects.all().order_by('-created')
    serializer_class = RecipeSerializer

    @list_route()
    def latest(self, request, number=5):
        queryset = self.queryset[:int(number)]
        serializer = RecipeSerializer(queryset, many=True)
        return Response(serializer.data)



class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    queryset = Ingredient.objects.all().order_by('-created')
    serializer_class = IngredientSerializer


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    queryset = RecipeIngredient.objects.all().order_by('-created')
    serializer_class = RecipeIngredientSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import list_route

from recipedb.models import Recipe, Ingredient, RecipeIngredient, UNITS
from recipedb.serializers import RecipeSerializer, IngredientSerializer, RecipeIngredientSerializer, UserSerializer, \
    UnitSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    queryset = Recipe.objects.all().order_by('-created')
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    queryset = RecipeIngredient.objects.all().order_by('-created')
    serializer_class = RecipeIngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UnitViewSet(viewsets.GenericViewSet):
    queryset = map(lambda x: {'abbr': x[0], 'name': x[1]}, UNITS)

    def list(self, request):
        queryset = map(lambda x: {'abbr': x[0], 'name': x[1]}, UNITS)
        serializer = UnitSerializer(queryset, many=True)
        return Response(serializer.data)
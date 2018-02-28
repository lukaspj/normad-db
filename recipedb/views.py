from django.contrib.auth.models import User
from drf_haystack.viewsets import HaystackViewSet
from rest_framework import viewsets, permissions, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import list_route

from recipedb.models import Recipe, Ingredient, RecipeIngredient, UNITS
from recipedb.permissions import IsStaffOrTargetUser
from recipedb.serializers import RecipeSerializer, IngredientSerializer, RecipeIngredientSerializer, UserSerializer, \
    UnitSerializer, RecipeSearchSerializer, IngredientSearchSerializer


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

    def search(self, request, number=5):
        queryset = self.queryset.order_by()


class RecipeSearchView(HaystackViewSet):
    index_models = [Recipe]

    serializer_class = RecipeSearchSerializer

class IngredientSearchView(HaystackViewSet):
    index_models = [Ingredient]

    serializer_class = IngredientSearchSerializer


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

    def get_permissions(self):
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)
        else:
            return (IsStaffOrTargetUser(),)


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }

class UnitViewSet(viewsets.GenericViewSet):
    queryset = map(lambda x: {'abbr': x[0], 'name': x[1]}, UNITS)

    def list(self, request):
        queryset = map(lambda x: {'abbr': x[0], 'name': x[1]}, UNITS)
        serializer = UnitSerializer(queryset, many=True)
        return Response(serializer.data)
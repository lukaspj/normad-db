"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from recipedb import views as recipeviews

router = routers.DefaultRouter()
router.register(r'recipes/search', recipeviews.RecipeSearchView, base_name="recipe-search")
router.register(r'recipes', recipeviews.RecipeViewSet)
router.register(r'ingredients/search', recipeviews.IngredientSearchView, base_name="ingredient-search")
router.register(r'ingredients', recipeviews.IngredientViewSet)
router.register(r'recipeingredients', recipeviews.RecipeIngredientViewSet)
router.register(r'users', recipeviews.UserViewSet)
router.register(r'units', recipeviews.UnitViewSet, base_name='Units')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^recipes/latest/(?P<number>[0-9]+)/', recipeviews.RecipeViewSet.as_view({'get': 'latest'}), name='latest'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
]
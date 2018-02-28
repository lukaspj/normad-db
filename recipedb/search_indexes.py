from django.utils import timezone

from recipedb.models import Recipe, Ingredient

from haystack import indexes

class RecipeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    name = indexes.CharField(model_attr="name")
    created = indexes.DateTimeField(model_attr="created")


    def get_model(self):
        return Recipe

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(created__lte=timezone.now())

class IngredientIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    name = indexes.CharField(model_attr="name")
    created = indexes.DateTimeField(model_attr="created")

    def get_model(self):
        return Ingredient

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(created__lte=timezone.now())
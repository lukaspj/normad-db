from django.db import models

UNITS = [
    ('g', 'gram'),
    ('kg', 'kilogram'),
    ('l', 'liter'),
    ('dl', 'deciliter'),
    ('cl', 'centiliter'),
    ('tsk', 'teske'),
    ('spsk', 'spiseske'),
    ('stk', 'styk'),
]

class Recipe(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=256, blank=True, default='')
    image = models.URLField(blank=True, default='')
    steps = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=256, blank=True, default='')
    image = models.URLField(blank=True, default='')
    estprice = models.FloatField(null=True, default=None)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE, null=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    amount = models.FloatField()
    unit = models.CharField(choices=UNITS, max_length=32)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return "%s: %s" % (self.recipe, self.ingredient)

    def __unicode__(self):
        return "%s: %s" % (self.recipe, self.ingredient)
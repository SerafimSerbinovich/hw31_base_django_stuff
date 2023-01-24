from django.db import models


class AdModel(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=15)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=1000)
    address = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)


class CategoryModel(models.Model):
    name = models.CharField(max_length=200)

from django.db import models


class ItemCategory(models.Model):

    name = models.CharField(max_length=55)

    class Meta:
        verbose_name = ("itemcategory")
        verbose_name_plural = ("itemcategories")
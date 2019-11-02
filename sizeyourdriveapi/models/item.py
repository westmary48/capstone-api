from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .donator import Donator
from .itemcategory import ItemCategory
from .donationbox import DonationBox
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class Item(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE
    name = models.CharField(max_length=50,)
    donator = models.ForeignKey(Donator, on_delete=models.DO_NOTHING, related_name="items")
    size = models.CharField(max_length=50,)
    description = models.CharField(max_length=255,)
    quantity = models.IntegerField(validators=[MinValueValidator(0)],)
    created_date = models.DateField(default="0000-00-00",)
    item_category = models.ForeignKey(ItemCategory, on_delete=models.DO_NOTHING, related_name="item_category")


    class Meta:
        verbose_name = ("item")
        verbose_name_plural = ("items")
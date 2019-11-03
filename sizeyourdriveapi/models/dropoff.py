from django.db import models
from .donator import Donator
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class Dropoff(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE
    name = models.CharField(max_length=50,)
    organization = models.CharField(max_length=50,)
    donator = models.ForeignKey(Donator, on_delete=models.DO_NOTHING, )
    dropoff_date = models.DateField(default="0000-00-00",)
    create_date = models.DateField(default="0000-00-00",)

    class Meta:
        verbose_name = ("dropoff")
        verbose_name_plural = ("dropoffs")
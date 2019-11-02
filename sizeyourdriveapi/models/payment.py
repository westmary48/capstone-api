from django.db import models
from .donator import Donator
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class Payment(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE
    merchant_name = models.CharField(max_length=25,)
    account_number = models.CharField(max_length=25)
    donator = models.ForeignKey(Donator, on_delete=models.DO_NOTHING, )
    expiration_date = models.DateField(default="0000-00-00",)
    create_date = models.DateField(default="0000-00-00",)

    class Meta:
        verbose_name = ("payment")
        verbose_name_plural = ("payments")
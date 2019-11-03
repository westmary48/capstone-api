from django.db import models
from .donator import Donator
from .dropoff import Dropoff


class DonationBox(models.Model):
    donator = models.ForeignKey(Donator, on_delete=models.DO_NOTHING, related_name="donatordonationbox")
    dropoff = models.ForeignKey(Dropoff, on_delete=models.DO_NOTHING, null=True)
    created_date = models.DateField(default="0000-00-00",)



    class Meta:
        verbose_name = ("donationbox")
        verbose_name_plural = ("donationbox")

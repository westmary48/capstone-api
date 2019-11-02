from django.db import models
from .donator import Donator
from .payment import Payment


class DonationBox(models.Model):
    donator = models.ForeignKey(Donator, on_delete=models.DO_NOTHING, related_name="donatordonationbox")
    payment_type = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, null=True)
    created_date = models.DateField(default="0000-00-00",)



    class Meta:
        verbose_name = ("donationbox")
        verbose_name_plural = ("donationbox")

from django.db import models
from .donationbox import DonationBox
from .item import Item

class ItemDonationbox(models.Model):

    donationbox = models.ForeignKey("DonationBox", on_delete=models.DO_NOTHING, related_name="invoiceline")
    item = models.ForeignKey("Item", on_delete=models.DO_NOTHING, related_name="item")
    quantity = models.IntegerField()

    class Meta:
        verbose_name = ("itemdonationbox")
        verbose_name_plural = ("itemdonationboxes")
from django.db import models
from .customer import Customer

"""
Author: Galaydia Team
Purpose: Single source of information about Payment Type Data with essential fields to be stored in database.
This model maps to a Payment Type database table.
Method: None

"""

class PaymentType(models.Model):

    merchant_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=25)
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ("customer", )
        verbose_name = ("paymenttype")
        verbose_name_plural = ("paymenttypes")




from django.db import models
from .customer import Customer
from .paymenttype import PaymentType

class Order(models.Model):

    """
    Author: Galaydia Team
    Purpose: Single source of information about Order Data with essential fields to be stored in database.
    This model maps to a Order database table.
    Method: None

    """

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, blank=True, null=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    class Meta:
        ordering = ("customer", )
        verbose_name = ("order")
        verbose_name_plural = ("orders")


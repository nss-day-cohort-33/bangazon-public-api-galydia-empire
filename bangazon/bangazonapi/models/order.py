from django.db import models
from .customer import Customer
from .paymenttype import PaymentType

"""
Author: Galaydia Team
Purpose: Single source of information about Order Data with essential fields to be stored in database.
This model maps to a Order database table.
Method: None

"""
class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING)
    created_at = models.DateField()
    completed = models.BooleanField()


    class Meta:
        ordering = ("customer", )
        verbose_name = ("order")
        verbose_name_plural = ("orders")
from django.db import models

"""
Author: Galaydia Team
Purpose: Single source of information about Product Orders Data with essential fields to be stored in database.
This model maps to a Order Product database table.
Method: None

"""
class OrderProduct(models.Model):

    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="cart")
    product= models.ForeignKey("Product", on_delete=models.CASCADE, related_name="cart")

    class Meta:
        ordering = ("order", )
        verbose_name = ("orderproduct")
        verbose_name_plural = ("orderproducts")




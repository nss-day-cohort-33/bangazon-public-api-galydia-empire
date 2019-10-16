from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .customer import Customer
from .producttype import ProductType

"""
Author: Galaydia Team
Purpose: Single source of information about Product Data with essential fields to be stored in database.
This model maps to a Product database table.
Method: None

"""
class Product(models.Model):

    name = models.CharField(max_length=50)
    price = models.FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(10000.00)],)
    description = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ("product_type", )
        verbose_name = ("product")
        verbose_name_plural = ("products")




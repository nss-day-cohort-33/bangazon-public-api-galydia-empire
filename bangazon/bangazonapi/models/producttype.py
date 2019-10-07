from django.db import models

"""
Author: Galaydia Team
Purpose: Single source of information about Product Type Data with essential fields to be stored in database.
This model maps to a Product Type database table.
Method: None

"""

class ProductType(models.Model):

    name = models.CharField(max_length=50)

    class Meta:
        ordering = ("name", )
        verbose_name = ("producttype")
        verbose_name_plural = ("producttypes")

    def __str__(self):
        return self.name
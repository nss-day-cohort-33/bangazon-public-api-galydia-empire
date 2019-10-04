from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
Author: Galaydia Team
Purpose: Single source of information about Customer Data with essential fields to be stored in database.
This model maps to a Customer database table.
Method: None

"""

class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=25)

    # def __str__(self):
    #     return "{} {}".format(self.first_name, self.last_name)

    # class Meta:
    #     ordering = (F('user.date_joined').asc(nulls_last=True),)

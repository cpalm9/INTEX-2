

# ACCOUNT APP

from django.contrib.auth.models import AbstractUser

from django.db import models
from catalog import models as cmod
import random


class FomoUser(AbstractUser):
    birth_date = models.DateField(null=True)
    phone = models.TextField(max_length = 14)
    address = models.TextField()
    city = models.TextField()
    state = models.CharField(max_length = 2)
    zipcode = models.TextField()
    shipping_address = models.TextField(blank=True, null=True)
    # add more fields

    def get_cart_count(self):
        #get number from database

        cart_count = cmod.ShoppingCartItems.objects.filter(user_id=self.id)

        counter = 0

        for c in cart_count:
            if hasattr(c.product, 'quantity'):
                counter += c.quantity
            else:
                counter += 1

        return counter



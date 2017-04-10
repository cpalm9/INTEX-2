

# ACCOUNT APP

from django.contrib.auth.models import AbstractUser

from django.db import models

class FomoUser(AbstractUser):
    birth_date = models.DateField(null=True)
    phone = models.TextField(max_length = 14)
    address = models.TextField()
    city = models.TextField()
    state = models.CharField(max_length = 2)
    zipcode = models.TextField()
    # add more fields






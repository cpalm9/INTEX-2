from django.db import models
from polymorphic.models import PolymorphicModel
# Create your models here.

class Category(models.Model):
    #id
    code = models.TextField(blank = True, null = True)
    name = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.name



class Product(PolymorphicModel):
    #id
    price = models.DecimalField(max_digits = 8, decimal_places = 2, blank = True, null = True) #999,999.99
    name = models.TextField(blank = True, null =True)
    brand = models.TextField(blank = True, null = True)
    category = models.ForeignKey('Category')
    create_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)
    # class Meta:
    #     abstract = True


class BulkProduct(Product):
    #id
    quantity = models.IntegerField(default = 0)
    reorder_trigger = models.IntegerField(default = 0)
    reorder_qty = models.IntegerField(default = 0)
    #vendor

class UniqueProduct(Product):
    #id
    serial_number = models.TextField(blank = True, null = True)
    #vendor

class RentalProduct(Product):
    #id
    serial_number = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=0)

class ProductPicture(models.Model):
    product = models.ForeignKey('Product')
    path = models.TextField()
#     altText = models.TextField()
#     mimeType = models.TextField()
        #img/jpg, img/png, img/gif

# Three things objects have: Methods, Data, Identity

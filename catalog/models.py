from polymorphic.models import PolymorphicModel
from account import models
from django.db import models
from decimal import Decimal

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
    path = models.TextField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
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
    active = models.BooleanField(default=True)
    #vendor

class RentalProduct(Product):
    #id
    serial_number = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=1)

class ProductPicture(models.Model):
    product = models.ForeignKey('Product')
    path = models.TextField()
#     altText = models.TextField()
#     mimeType = models.TextField()
        #img/jpg, img/png, img/gif

class ShoppingHistory(models.Model):
    product = models.ForeignKey('Product', null=True)
    user = models.ForeignKey('account.FomoUser', null=True)
    date_viewed = models.DateTimeField(auto_now = True)

class ShoppingCartItems(models.Model):
    product = models.ForeignKey('Product', null=True)
    user = models.ForeignKey('account.FomoUser', null=True)
    quantity = models.IntegerField(default = 0, null=True)
    extended_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True)


class Sales(models.Model):
    user = models.ForeignKey('account.FomoUser', null=True)
    date = models.DateTimeField(auto_now = True, null=True)
    shipping_address = models.TextField(blank=False, null=False)
    total_cost = models.DecimalField(max_digits=6, decimal_places=2)

    @staticmethod
    def record_sale(user, cart_items, address, stripe_token, sale_id):

        sale = Sales()
        sale.user = user
        sale.shipping_address = address


        sale.total_cost = SaleItems.calc_total()

        sale.save()

        saleItem = SaleItems()
        for s in cart_items:
            saleItem.product = s.product
            saleItem.sale = sale
            saleItem.quantity_purchased = s.quantity
            saleItem.sale_price = s.product.price
            saleItem.tax = round(s.product.price * Decimal(.075), 2)
            saleItem.shipping_cost = 10

            saleItem.save()

        payment = Payment()
        payment.sale = sale
        payment.stripe_token = stripe_token
        payment.amount = sale.total_cost
        payment.save()



        for s in cart_items:
            product = Product.objects.get(id=s.product.id)
            if hasattr(s.product, 'quantity'):
                product.quantity -= s.quantity
            elif hasattr(s.product, 'active'):
                product.active = False

            product.save()

        sale_id['value'] = sale.id

class SaleItems(models.Model):
    product = models.ForeignKey('Product', null=True)
    sale = models.ForeignKey('Sales', null=True)
    quantity_purchased = models.IntegerField(null=True, blank=False)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    tax = models.DecimalField(max_digits=6, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2)

    @staticmethod
    def calc_subtotal():
        cartItems = ShoppingCartItems.objects.all()

        subtotal = 0
        for s in cartItems:
            subtotal += s.extended_amount

        return subtotal

    @staticmethod
    def calc_tax():
        tax = round(SaleItems.calc_subtotal() * Decimal(0.0725), 2)
        return tax

    @staticmethod
    def calc_total():
        total = (SaleItems.calc_subtotal() + SaleItems.calc_tax() + 10)
        return total

    @staticmethod
    def clear_cart(user):
        product = ShoppingCartItems.objects.filter(user=user)
        for p in product:
            p.delete()



class Payment(models.Model):
    sale = models.ForeignKey('Sales', null=True)
    stripe_token = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now = True, null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)


# Three things objects have: Methods, Data, Identity

from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string
from catalog import models as cmod
from account import models as amod
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required
from django import forms
from formlib.form import FormMixIn
from decimal import Decimal

@view_function
def process_request(request):
    #pull product from the db
    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])
    except:
        return HttpResponseRedirect('/catalog/index/')

    try:
        productImage = cmod.ProductPicture.objects.filter(product=product)

    except cmod.ProductPicture.DoesNotExist:
        return HttpResponseRedirect('/catalog/index/')

    user = request.user

    history = cmod.ShoppingHistory()

    try:
        history.user = user

    except:
        history.user = None

    history.product = product
    history.save()



    #add to the last 5 viewed items
    #check to see if product is already in list
    # if [product.name, product.id] not in request.last5:
    #     request.last5.insert(0, [product.name, product.id])
    # else:
    #     request.last5.insert(0, request.last5.pop(request.last5.index([product.name, product.id])))
    #
    # while len(request.last5) > 5:
    #     request.last5.pop()

    form = BuyNowForm(request, product=product)
    if form.is_valid():
        form.commit(product, user)




    context = {
        'product': product,
        'productImage': productImage,
        'form': form,

    }

    return dmp_render(request, 'details-ajax.html' if request.method == 'POST' else 'details.html', context)


class BuyNowForm(FormMixIn, forms.Form):

    form_submit = 'Add To Cart'
    form_id = 'buy_now_form'

    def init(self, product):
        # fields
        if hasattr(product, 'quantity'):
            self.fields['quantity'] = forms.IntegerField(required=False)

    def clean(self):

        shoppingItems = cmod.ShoppingCartItems.objects.all()

        qty = self.cleaned_data.get('quantity')

        id = self.request.urlparams[0]

        product = cmod.Product.objects.get(id=id)

        if hasattr(product, 'quantity'):
            for s in shoppingItems:
                if int(id) == int(s.product.id):
                    if product.quantity < s.quantity:
                        raise forms.ValidationError('Invalid Quantity')
                else:
                    if product.quantity < qty:
                        raise forms.ValidationError('Invalid Quantity')

        else:
            for s in shoppingItems:
                #For some reason these aren't originally the same data type
                if int(id) == int(s.product.id):
                    raise forms.ValidationError('Item no longer available')


        # clean the qty here (this would normally be a DB call)
        # Do the logic to make sure they can't buy more that what is available.
        return self.cleaned_data

    def commit(self, product, user):

        shoppingItems = cmod.ShoppingCartItems.objects.filter(user=user)

        duplicate = False

        for s in shoppingItems:
            if s.product.id == product.id:
                if hasattr(s.product, 'quantity'):
                    s.quantity += self.cleaned_data.get('quantity')
                    s.extended_amount += Decimal(self.cleaned_data.get('quantity') * product.price)
                else:
                    s.quantity += 1
                duplicate = True
                s.save()
                break
            else:
                duplicate = False

        if duplicate == False:
            cartItem = cmod.ShoppingCartItems()
            cartItem.product = product
            cartItem.quantity = self.cleaned_data.get('quantity')
            cartItem.user = user
            if hasattr(product, 'quantity'):
                cartItem.extended_amount = Decimal(self.cleaned_data.get('quantity') * product.price)
            else:
                cartItem.extended_amount = product.price
            cartItem.save()

        # connect the request object and the user object
        # ret = stripe.Charge.create(... inc token id)
        # record_sale(charge_token, self.request.user...)
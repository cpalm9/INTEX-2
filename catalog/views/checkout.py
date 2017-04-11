from django.conf import settings
from django_mako_plus import view_function
from django.http import HttpResponse, HttpResponseRedirect
from account import models as amod
from django import forms
from catalog import models as cmod
from formlib.form import FormMixIn
from django.contrib.auth.decorators import permission_required, login_required
from decimal import Decimal
import stripe


from .. import dmp_render, dmp_render_to_string


@view_function
@login_required
def process_request(request):

    checklist = cmod.ShoppingCartItems.objects.filter(user=request.user)

    if not checklist:
        return HttpResponseRedirect('/catalog/index/')

    user = request.user

    form = CheckoutForm(request)

    if form.is_valid():
        sale_id = {'value': ''}
        form.commit(user, sale_id)

        return HttpResponseRedirect('/catalog/receipt/' + str(sale_id['value'])) #take them back to /catalog/receipt/

    context = {
        'form': form,
        'checklist': checklist,
    }

    return dmp_render(request, 'checkout.html', context)


class CheckoutForm(FormMixIn, forms.Form):
    form_submit = 'Pay Now'
    def init(self):
        self.fields['stripe_token'] = forms.CharField(required=False, widget = forms.HiddenInput())


    def commit(self, user, sale_id):
        print('>>>>>>> Checkout works!')

        cart_items = cmod.ShoppingCartItems.objects.all()
        address = amod.FomoUser.objects.get(id=user.id).shipping_address
        stripe_token = self.cleaned_data.get('stripe_token')

        cmod.Sales.record_sale(user, cart_items, address, stripe_token, sale_id)

        # amount = str(Decimal(cmod.Sales.objects.get(id=sale_id).total_cost))
        amount = cmod.SaleItems.calc_total()
        print('$$$$$$$$$$$$$$$$', amount)
        cmod.SaleItems.clear_cart(user)
        stripe.api_key = settings.STRIPE_SECRET_KEY

        stripe.Charge.create(
            amount=int(amount * 100),
            currency="usd",
            source=stripe_token,  # obtained with Stripe.js
            description="Charge for FOMO instruments"
        )
        

        #Charge the token in stripe
        # ret = stripe.Charge.create(use token id)
        # create the sale object
        # create saleitem objects
        # update quantities
        # empty shopping cart

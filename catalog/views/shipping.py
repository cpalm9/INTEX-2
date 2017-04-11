
from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from account import models as amod
from django import forms
from formlib.form import FormMixIn
from django.contrib.auth import authenticate, login
from catalog import models as cmod
from account import models as amod
import googlemaps
from django.contrib.auth.decorators import permission_required, login_required
import json


from .. import dmp_render, dmp_render_to_string


@view_function
@login_required
def process_request(request):

    checklist = cmod.ShoppingCartItems.objects.filter(user=request.user)

    if not checklist:
        return HttpResponseRedirect('/catalog/index/')

    user = request.user

    form = ShippingForm(request)

    if form.is_valid():
        form.commit(user)

        return HttpResponseRedirect('/catalog/checkout/')

    context = {
        'checklist': checklist,
        'form': form,
    }

    return dmp_render(request, 'shipping.html', context)


class ShippingForm(FormMixIn, forms.Form):

    def init(self):
        self.fields['street'] = forms.CharField(label='Street Address', required=True)
        self.fields['city'] = forms.CharField(label='City', required=True)
        self.fields['state'] = forms.CharField(label='State', required=True)
        self.fields['zipcode'] = forms.CharField(label='Zipcode', required=True)

        # self.fields['stripe_token'] = forms.CharField(required=False) #widget = forms.HiddenInput()


    def clean(self):



        gmaps = googlemaps.Client(key=settings.GOOGLE_SERVER_KEY)

        street = self.cleaned_data.get('street')
        city = self.cleaned_data.get('city')
        state = self.cleaned_data.get('state')
        zipcode = self.cleaned_data.get('zipcode')

        full_address = street + ', ' + city + ', ' + state + ', ' + str(zipcode)

        # Geocoding an address
        geocode_result = gmaps.geocode(full_address)

        if geocode_result == []:
            raise forms.ValidationError('Please enter valid address')

        address_result1 = geocode_result[0]["address_components"][0]["long_name"]
        address_result2 = geocode_result[0]["address_components"][1]["long_name"]

        # new_address = address_result1 + ' ' + address_result2
        # new_city = geocode_result[0]["address_components"][2]["long_name"]
        # new_state = geocode_result[0]["address_components"][4]["long_name"]
        # new_zip = geocode_result[0]["address_components"][6]["long_name"]
        # new_full_address = new_address + ', ' + new_city + ', ' + new_state + ', ' + new_zipcode

        google_address = geocode_result[0]['formatted_address']
        address_list = [x.strip() for x in google_address.split(',')]
        # print(address_list)
        new_address = address_list[0]
        new_city = address_list[1]
        new_state = ''.join(c for c in address_list[2] if c.isalpha())
        new_zipcode = ''.join(c for c in address_list[2] if c.isdigit())
        new_full_address = new_address + ', ' + new_city + ', ' + new_state + ', ' + new_zipcode

        self.data = self.data.copy()
        if full_address == new_full_address:
            return self.cleaned_data
        else:
            self.data['street'] = new_address
            self.data['city'] = new_city
            self.data['state'] = new_state
            self.data['zipcode'] = new_zipcode
            raise forms.ValidationError('We have made some changes please make sure it is correct.')

        return self.cleaned_data


    def commit(self, user):
        print('>>>>>>> Checkout works!')

        thisUser = amod.FomoUser.objects.get(id=user.id)

        thisUser.shipping_address = self.data['street'] + ' ' + self.data['city'] + ' ' + self.data['state'] + ' ' + self.data['zipcode']

        thisUser.save()

        #Charge the token in stripe
        # ret = stripe.Charge.create(use token id)
        # create the sale object
        # create saleitem objects
        # update quantities
        # empty shopping cart

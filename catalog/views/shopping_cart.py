from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string
from catalog import models as cmod
from django_mako_plus import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_string
from catalog import models as cmod
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from formlib.form import FormMixIn
from django.contrib.auth.decorators import permission_required, login_required




@view_function
def process_request(request):

    products = cmod.ShoppingCartItems.objects.filter(user=request.user)

    context = {'products': products}

    return dmp_render(request, 'shopping_cart.html', context)



############################ Delete Function ########################################

@view_function
def delete(request):
    try:
        product = cmod.ShoppingCartItems.objects.get(id=request.urlparams[0])

    except cmod.ShoppingCartItems.DoesNotExist:
        return HttpResponseRedirect('/catalog/shopping_cart/')

    product.delete()
    return HttpResponseRedirect('/catalog/shopping_cart/')

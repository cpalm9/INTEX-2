from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_string
from catalog import models as cmod
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required



@view_function
@login_required
def process_request(request):
    #pull all products from the db
    products = cmod.Product.objects.order_by('name').all()

    #
    # try:
    #     p = cmod.Product.objects.get(id = 000000)
    #
    # except cmod.Product.DoesNotExist:
    #     return HttpResponseRedirect('/manager/products')
    #
    #

    #render the template
    context = {
        'products': products,
    }

    print(products)


    return dmp_render(request, 'products.html', context)




@view_function
def get_quantity(request):
    # returns the current quantity for a given product id
    pid = request.urlparams[0]


    try:
        p = cmod.Product.objects.get(id = request.urlparams[0])

    except cmod.Product.DoesNotExist:
        return HttpResponseRedirect('/manager/products')

    return HttpResponse(p.quantity)

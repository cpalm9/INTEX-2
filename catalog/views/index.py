from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_string
from catalog import models as cmod
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required



@view_function
def process_request(request):
    #pull all products from the db
    products = cmod.Product.objects.order_by('name').all()

    if request.urlparams[0] != '':
        products = products.filter(category=request.urlparams[0])

    #render the template
    context = {
        'products': products,
    }

    return dmp_render(request, 'index.html', context)
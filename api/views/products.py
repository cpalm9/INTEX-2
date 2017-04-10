from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_string
from catalog import models as cmod
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
import json
from django import forms
from formlib.form import FormMixIn
import decimal



@view_function
def process_request(request):



    product = cmod.Product.objects.all()
    product_list = {'product': [], 'errors': []}

    if request.GET.get('name'):
        if request.GET.get('name').isalpha():
            product = product.filter(name__icontains=request.GET.get('name', ''))
        else:
            product_list['errors'].append('INVALID INPUT')


    if request.GET.get('min_price'):
        if request.GET.get('min_price').isalpha():
            product = product.filter(price__gte=request.GET.get('min_price'))
        else:
            product_list['errors'].append('INVALID PRICE INPUT')

    if request.GET.get('max_price'):
        if request.GET.get('max_price').isdigit():
            product = product.filter(price__lte=request.GET.get('max_price'))
        else:
            product_list['errors'].append('INVALID PRICE INPUT')

    if request.GET.get('category'):
        if request.GET.get('category').isalpha():
            product = product.filter(category__name__icontains=request.GET.get('category', ''))
        else:
            product_list['errors'].append('INVALID INPUT')




    for p in product:
        if not product_list['errors']:
            ret = {
                'price': p.price,
                'name': p.name,
                'brand': p.brand,
                'quantity': getattr(p, 'quantity', 0),
                'category': p.category.name,
            }

            product_list['product'].append(ret)
            status = 200
        else:
            status = 400



    return JsonResponse(product_list, status=status)



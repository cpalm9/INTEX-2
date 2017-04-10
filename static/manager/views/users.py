from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_string
from account import models as amod
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponse, HttpResponseRedirect



@view_function
@login_required
def process_request(request):
    #pull all users from the db
    users = amod.FomoUser.objects.order_by('first_name').all()

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
        'users': users,
    }

    print(users)


    return dmp_render(request, 'users.html', context)
from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_string
from catalog import models as cmod
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required
from django.core.mail import send_mail


@view_function
def process_request(request):
    #pull all products from the db
    try:
        sale = cmod.Sales.objects.get(id=request.urlparams[0])

    except cmod.Sales.DoesNotExist:
        return HttpResponseRedirect('/catalog/index/')

    send_mail(
        'Subject here',
        'Here is the message.',
        'mail@familymusic.club',
        ['sburnham92@gmail.com'],
        fail_silently=False,
    )




    #render the template
    context = {
        'sale': sale,
    }

    return dmp_render(request, 'receipt.html', context)
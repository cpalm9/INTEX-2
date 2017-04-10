
from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from account import models as amod
from django import forms
from formlib.form import FormMixIn
from django.contrib.auth import authenticate, login

from .. import dmp_render, dmp_render_to_string


@view_function
def process_request(request):
    user = request.user

    context = {
        'user': user,
    }

    return dmp_render(request, 'index.html', context)

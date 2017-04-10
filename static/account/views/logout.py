# from django.contrib.auth import logout
from django .http import HttpResponseRedirect
from django_mako_plus import view_function
from django.contrib.auth import logout
from django.shortcuts import redirect

@view_function
def process_request(request):
    logout(request)

    return HttpResponseRedirect('/homepage/index/')
from django.conf import settings
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string
from datetime import datetime
import random

@view_function
def process_request(request):
    context = {
    }
    return dmp_render(request, 'about.html', context)
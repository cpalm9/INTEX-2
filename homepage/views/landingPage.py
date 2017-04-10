from django.conf import settings
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string
from datetime import datetime
import random

@view_function
def process_request(request):
    context = {
        'now': datetime.now().strftime(request.urlparams[0] if request.urlparams[0] else '%Y'),
        'timecolor': random.choice([ 'red', 'blue', 'green', 'brown' ]),
    }
    return dmp_render(request, 'landingPage.html', context)
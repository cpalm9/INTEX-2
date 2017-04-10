from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_string
from account import models as amod
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from formlib.form import FormMixIn
from django.contrib.auth.decorators import permission_required, login_required

@view_function
@permission_required('admin')
def process_request(request):
    try:
        user = amod.FomoUser.objects.get(id=request.urlparams[0])

    except amod.FomoUser.DoesNotExist:
        return HttpResponseRedirect('/manager/users/')

    # process the form
    form = EditPasswordForm(request, user=user)

    if form.is_valid():
        print('>>>>>>>>>>>>>> Valid Form')
        form.commit(user)
        return HttpResponseRedirect('/manager/users/')

    # render the template
    context = {
        'user': user,
        'form': form,
    }
    return dmp_render(request, 'editPassword.html', context)


class EditPasswordForm(FormMixIn, forms.Form):

    def init(self, user):
        self.fields['new_password'] = forms.CharField(widget=forms.PasswordInput())
        self.fields['new_password2'] = forms.CharField(widget=forms.PasswordInput())



    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        if self.cleaned_data.get('new_password') != self.cleaned_data.get('new_password2'):
            print('>>>>>>>>>>>>>> ' + new_password)
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data



    def commit(self, user):
        print('>>>>>>>>>>>>>> Valid Form')
        user.set_password(self.cleaned_data.get('new_password'))
        user.save()

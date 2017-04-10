from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_string
from account import models as amod
from django import forms
from django.contrib.auth import authenticate, login
from formlib.form import FormMixIn
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required


@view_function
@login_required
def process_request(request):
    try:
        user = amod.FomoUser.objects.get(id=request.urlparams[0])

    except amod.FomoUser.DoesNotExist:
        return HttpResponseRedirect('/account/editAccount/')

    # process the form
    form = EditPasswordForm(request, user=user)
    form.user = authenticate(username=request.user.username, password=request.POST.get('old_password'))
    if form.is_valid():
        print('>>>>>>>>>>>>>> Valid Form')

        form.commit(user)
        login(request, user)

        return HttpResponseRedirect('/account/index/')

    # render the template
    context = {
        'user': user,
        'form': form,
    }
    return dmp_render(request, 'editAccount.html', context)


class EditPasswordForm(FormMixIn, forms.Form):

    def init(self, user):
        self.fields['old_password'] = forms.CharField(widget=forms.PasswordInput())
        self.fields['new_password'] = forms.CharField(widget=forms.PasswordInput())
        self.fields['new_password2'] = forms.CharField(widget=forms.PasswordInput())



    def clean(self):
        if self.user is None:
            raise forms.ValidationError("Incorrect current password")
        else:
            new_password = self.cleaned_data.get('new_password')
            if self.cleaned_data.get('new_password') != self.cleaned_data.get('new_password2'):
                print('>>>>>>>>>>>>>> ' + new_password)
                raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data



    def commit(self, user):
        print('>>>>>>>>>>>>>> Valid Form')
        user.set_password(self.cleaned_data.get('new_password'))
        user.save()

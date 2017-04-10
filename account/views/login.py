
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
    form = LoginForm(request)

    if form.is_valid():
        form.commit()
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/account/index/')
        else:
            return HttpResponseRedirect('/account/login/')

    context = {
        'form': form,
    }

    return dmp_render(request, 'login.html', context)


class LoginForm(FormMixIn, forms.Form):

    def init(self):
        self.form_action = '/account/login.modal/'
        self.fields['username'] = forms.CharField(label='Username', required=True)
        self.fields['password'] = forms.CharField(label='Password', required=True, widget=forms.PasswordInput())

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if username is None:
    #         raise forms.ValidationError('You did something wrong')
    #     return username
    #
    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if password is None:
    #         raise forms.ValidationError('You did something wrong again')
    #     return password

    def clean(self):
        user = authenticate(username=self.cleaned_data.get(
            'username'), password=self.cleaned_data.get('password'))
        if user is None:
            raise forms.ValidationError('Invalid Username or Password')
        return self.cleaned_data


    def commit(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

#Ajax

@view_function
def modal(request):
    form = LoginForm(request)

    if form.is_valid():
        form.commit()
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponse('''
                <script>
                    window.location.href = "/account/index/";
                </script>
            ''')
        else:
            return HttpResponse('/account/login.modal')

    context = {
        'form': form,
    }

    return dmp_render(request, 'login.modal.html', context)
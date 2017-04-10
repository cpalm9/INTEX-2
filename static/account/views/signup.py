from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_string
from account import models as amod
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from formlib.form import FormMixIn


@view_function
def process_request(request):

    # process the form
    form = CreateForm(request)

    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/account/login/')

    # render the template
    context = {
        'form': form,
    }

    return dmp_render(request, 'signup.html', context)

class CreateForm(FormMixIn, forms.Form):


    def init(self):
        self.fields['username'] = forms.CharField(label='Username')
        self.fields['first_name'] = forms.CharField(label='First Name')
        self.fields['last_name'] = forms.CharField(label='Last Name')
        self.fields['email'] = forms.EmailField(label='Email')
        self.fields['birth_date'] = forms.DateField(label='Birth Date')
        self.fields['phone'] = forms.CharField(label='Phone', max_length=14)
        self.fields['address'] = forms.CharField(label='Address')
        self.fields['city'] = forms.CharField(label='City')
        self.fields['state'] = forms.CharField(label='State')
        self.fields['zipcode'] = forms.CharField(label='Zipcode')
        self.fields['password'] = forms.CharField(label='Password', widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if amod.FomoUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def commit(self):
        print('>>>>> form is valid')
        user = amod.FomoUser()
        user.username = self.cleaned_data.get('username')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.birth_date = self.cleaned_data.get('birth_date')
        user.phone = self.cleaned_data.get('phone')
        user.address = self.cleaned_data.get('address')
        user.city = self.cleaned_data.get('city')
        user.state = self.cleaned_data.get('state')
        user.zipcode = self.cleaned_data.get('zipcode')
        user.set_password(self.cleaned_data.get('password'))
        user.save()
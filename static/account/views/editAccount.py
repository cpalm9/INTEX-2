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
    #pull user from the db

    try:
        user = amod.FomoUser.objects.get(id=request.urlparams[0])

    except amod.FomoUser.DoesNotExist:
        return HttpResponseRedirect('/account/index/')


    # process the form
    form = EditUserForm(request, user=user, initial={
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'birth_date': user.birth_date,
        'address': user.address,
        'city': user.city,
        'state': user.state,
        'zipcode': user.zipcode,
        'phone': user.phone,
        'email': user.email,


    })
    if form.is_valid():
        form.commit(user)
        return HttpResponseRedirect('/account/index/')



    #render the template
    context = {
        'user': user,
        'form': form,
    }


    return dmp_render(request, 'editAccount.html', context)


class EditUserForm (FormMixIn, forms.Form):

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if amod.FomoUser.objects.filter(username=username).exclude(id=request.user.id):


    def init(self, user):
        self.fields['username'] = forms.CharField(label='Username', max_length=100)
        self.fields['first_name'] = forms.CharField(label='First Name', max_length=100)
        self.fields['last_name'] = forms.CharField(label='Last Name', max_length=100)
        self.fields['birth_date'] = forms.DateField(label='Birthday')
        self.fields['address'] = forms.CharField(label='Address')
        self.fields['city'] = forms.CharField(label='City')
        self.fields['state'] = forms.CharField(label='State', max_length=2)
        self.fields['zipcode'] = forms.CharField(label='Zipcode')
        self.fields['phone'] = forms.CharField(label='Phone', max_length=14)
        self.fields['email'] = forms.EmailField(label='Email')


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if amod.FomoUser.objects.filter(username=username).exclude(id=self.request.urlparams[0]):
            raise forms.ValidationError('Username already exists')
        return username


    def commit(self, user):
        print('>>>>> form is valid')
        user.username = self.cleaned_data.get('username')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.birth_date = self.cleaned_data.get('birth_date')
        user.address = self.cleaned_data.get('address')
        user.city = self.cleaned_data.get('city')
        user.state = self.cleaned_data.get('state')
        user.zipcode = self.cleaned_data.get('zipcode')
        user.phone = self.cleaned_data.get('phone')
        user.email = self.cleaned_data.get('email')
        user.save()
from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_string
from account import models as amod
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from formlib.form import FormMixIn
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.decorators import permission_required, login_required


@view_function
@permission_required('change_fomouser')
def process_request(request):
    #pull user from the db

    try:
        user = amod.FomoUser.objects.get(id=request.urlparams[0])

    except amod.FomoUser.DoesNotExist:
        return HttpResponseRedirect('/manager/users/')


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
        # 'permissions': user.user_permissions.all(),


    })
    if form.is_valid():
        form.commit(user)
        return HttpResponseRedirect('/manager/users/')



    #render the template
    context = {
        'user': user,
        'form': form,
    }


    return dmp_render(request, 'user.html', context)


class EditUserForm (FormMixIn, forms.Form):




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
        # self.fields['permissions'] = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required=False)


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
        # user.user_permissions.set(self.cleaned_data.get('permissions'))
        user.save()

###################################### CREATE FUNCTION ############################################

@view_function
@permission_required('add_fomouser')
def create(request):

    # process the form
    form = CreateForm(request)

    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/manager/users/')

    # render the template
    context = {
        'form': form,
    }

    return dmp_render(request, 'user.html', context)


class CreateForm(FormMixIn, forms.Form):

    GROUPS = [
        ['Manager', 'Manager'],
        ['Admin', 'Admin'],
    ]

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
        self.fields['groups'] = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)


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
        user.groups.set(self.cleaned_data.get('groups'))


###################################### DELETE FUNCTION ############################################

@view_function
@permission_required('delete_fomouser')
def delete(request):
    try:
        user = amod.FomoUser.objects.get(id=request.urlparams[0])

    except amod.FomoUser.DoesNotExist:
        return HttpResponseRedirect('/manager/users/')

    user.delete()
    return HttpResponseRedirect('/manager/users/')


from django.conf import settings
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string
from django.http import HttpResponseRedirect
from django import forms
from formlib.form import FormMixIn
from django.contrib import messages
from django.core.validators import validate_email

@view_function
def process_request(request):
    form = ContactForm(request)

    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/contact/')

    user = request.user
    print(user.groups)

    return dmp_render(request, 'contact.html',{
        'form': form,
    })

class ContactForm(FormMixIn, forms.Form):
    SUBJECT_CHOICES = [
        ['payment', 'payment issue'],
        ['login', "I can't login"],
        ['technical', 'I have a technical issue'],
        ['upset', 'I am upset at something'],
    ]


    def init(self):
        self.fields['name'] = forms.CharField(label='Name', max_length=100)
        self.fields['email'] = forms.EmailField(label='Email', max_length=100)
        self.fields['subject'] = forms.ChoiceField(label='Subject', choices=ContactForm.SUBJECT_CHOICES)
        self.fields['message'] = forms.CharField(label='Message', max_length=1000, widget=forms.Textarea())

    def clean_name(self):
        name = self.cleaned_data.get('name')
        #do the validation
        parts = name.split()
        if len(parts) <= 1:
            raise forms.ValidationError('Please give you first and last name.')
        # validate email
        # validate_email(self.cleaned_data.get('email'))


        #return the value
        return self.cleaned_data


    def commit(self):
        # if all works out then do the work
        email = self.cleaned_data.get('email')
        print(email)



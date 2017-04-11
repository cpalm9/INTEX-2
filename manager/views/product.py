from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_string
from catalog import models as cmod
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from formlib.form import FormMixIn
from django.contrib.auth.decorators import permission_required, login_required


@view_function
@permission_required('change_product')
def process_request(request):
    #pull product from the db

    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])

    except cmod.Product.DoesNotExist:
        return HttpResponseRedirect('/manager/products/')


    # process the form
    form = EditProductForm(request, product=product, initial={
        'name': product.name,
        'category': product.category,
        'price': product.price,
        'quantity': getattr(product, 'quantity', 0),


    })
    if form.is_valid():
        form.commit(product)
        return HttpResponseRedirect('/manager/products/')



    #render the template
    context = {
        'product': product,
        'form': form,
    }


    return dmp_render(request, 'product.html', context)


class EditProductForm (FormMixIn, forms.Form):


    def init(self, product):
        self.fields['name'] = forms.CharField(label='Product Name', max_length=100)
        self.fields['category'] = forms.ModelChoiceField(label='Category', queryset=cmod.Category.objects.order_by('name').all())
        self.fields['price'] = forms.DecimalField(label='Price' )

        if hasattr(product, 'quantity'):
            self.fields['quantity'] = forms.IntegerField(label='Quantity')



    def commit(self, product):
        print('>>>>> form is valid')
        product.name = self.cleaned_data.get('name')
        product.category = self.cleaned_data.get('category')
        product.price = self.cleaned_data.get('price')

        if hasattr(product, 'quantity'):
            product.quantity = self.cleaned_data.get('quantity')
        product.save()

###################################### CREATE FUNCTION ############################################

@view_function
@permission_required('add_product')
def create(request):

    # process the form
    form = CreateForm(request)

    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/manager/products/')

    # render the template
    context = {
        'form': form,
    }

    return dmp_render(request, 'product.html', context)

class CreateForm(FormMixIn, forms.Form):

    TYPE_CHOICES = [
        ['bulk' , 'Bulk Product'],
        ['unique' , 'Unique Product'],
    ]


    def init(self):
        self.fields['type'] = forms.ChoiceField(label='Product Type', choices = CreateForm.TYPE_CHOICES)
        self.fields['category'] = forms.ModelChoiceField(label='Category', queryset=cmod.Category.objects.order_by('name').all())
        self.fields['name'] = forms.CharField(label='Product Name', max_length=100)
        self.fields['brand'] = forms.CharField(label='Brand', max_length=100)
        self.fields['desc'] = forms.CharField(label='Description', max_length=800)
        self.fields['price'] = forms.DecimalField(label='Price' )
        self.fields['quantity'] = forms.IntegerField(label='Quantity', required=False)
        self.fields['reorder_trigger'] = forms.IntegerField(label='Reorder Trigger Point', required=False)
        self.fields['reorder_qty'] = forms.IntegerField(label='Reorder Quantity', required=False)
        self.fields['serial_number'] = forms.CharField(label='Serial Number', required=False)


    def commit(self):
        print('>>>>> form is valid')
        if(self.cleaned_data.get('type') == 'bulk'):
            bp = cmod.BulkProduct()
            bp.category = self.cleaned_data.get('category', None)
            bp.name = self.cleaned_data.get('name')
            bp.brand = self.cleaned_data.get('brand')
            bp.desc = self.cleaned_data.get('desc')
            bp.price = self.cleaned_data.get('price')
            bp.quantity = self.cleaned_data.get('quantity')
            bp.reorder_trigger = self.cleaned_data.get('reorder_trigger')
            bp.reorder_qty = self.cleaned_data.get('reorder_qty')
            bp.save()

        elif (self.cleaned_data.get('type') == 'unique'):
            up = cmod.UniqueProduct()
            up.category = self.cleaned_data.get('category', None)
            up.name = self.cleaned_data.get('name')
            up.brand = self.cleaned_data.get('brand')
            up.desc = self.cleaned_data.get('desc')
            up.price = self.cleaned_data.get('price')
            up.serial_number = self.cleaned_data.get('serial_number')
            up.save()

        elif (self.cleaned_data.get('type') == 'rental'):
            rp = cmod.RentalProduct()
            rp.category = self.cleaned_data.get('category', None)
            rp.name = self.cleaned_data.get('name')
            rp.brand = self.cleaned_data.get('brand')
            rp.desc = self.cleaned_data.get('desc')
            rp.price = self.cleaned_data.get('price')
            rp.quantity = self.cleaned_data.get('quantity')
            rp.serial_number = self.cleaned_data.get('serial_number')
            rp.save()


###################################### DELETE FUNCTION ############################################

@view_function
@permission_required('delete_product')
def delete(request):
    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])

    except cmod.Product.DoesNotExist:
        return HttpResponseRedirect('/manager/products/')

    product.delete()
    return HttpResponseRedirect('/manager/products/')

from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string
from catalog import models as cmod
from account import models as amod
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required
from django import forms
from django.core.validators import MinValueValidator
from formlib.form import FormMixIn
from decimal import Decimal

@view_function
def process_request(request):
    #pull product from the db
    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])
    except:
        return HttpResponseRedirect('/catalog/index/')

    try:
        productImage = cmod.ProductPicture.objects.filter(product=product)

    except cmod.ProductPicture.DoesNotExist:
        return HttpResponseRedirect('/catalog/index/')

    user = request.user

    history = cmod.ShoppingHistory()

    try:
        history.user = user

    except:
        history.user = None

    history.product = product
    history.save()

    comments =  cmod.ProductComment.objects.filter(product_id=product.id)
    print(comments)

    comment_form = CommentForm(request)
    print('HERE')
    if comment_form.is_valid():
        print('FORM CHECKS OUT')
        comment_form.commit(product=product)
        return HttpResponseRedirect('/catalog/details/' + str(product.id))

    form = BuyNowForm(request, product=product)
    if form.is_valid():
        form.commit(product, user)




    context = {
        'product': product,
        'productImage': productImage,
        'form': form,
        'comments': comments,
        'comment_form': comment_form,

    }

    return dmp_render(request, 'details-ajax.html' if request.method == 'POST' else 'details.html', context)


class BuyNowForm(FormMixIn, forms.Form):

    form_submit = 'Add To Cart'
    form_id = 'buy_now_form'

    def init(self, product):
        # fields
        if hasattr(product, 'quantity'):
            self.fields['quantity'] = forms.IntegerField(required=False, validators=[MinValueValidator(1)], initial=1)

    def clean(self):

        shoppingItems = cmod.ShoppingCartItems.objects.all()

        qty = self.cleaned_data.get('quantity')

        id = self.request.urlparams[0]

        product = cmod.Product.objects.get(id=id)

        if hasattr(product, 'quantity'):
            for s in shoppingItems:
                if int(id) == int(s.product.id):
                    if product.quantity < s.quantity:
                        raise forms.ValidationError('Invalid Quantity')
                else:
                    if product.quantity < qty:
                        raise forms.ValidationError('Invalid Quantity')

        else:
            for s in shoppingItems:
                #For some reason these aren't originally the same data type
                if int(id) == int(s.product.id):
                    raise forms.ValidationError('Item no longer available')


        # clean the qty here (this would normally be a DB call)
        # Do the logic to make sure they can't buy more that what is available.
        return self.cleaned_data

    def commit(self, product, user):

        shoppingItems = cmod.ShoppingCartItems.objects.filter(user=user)

        duplicate = False

        for s in shoppingItems:
            if s.product.id == product.id:
                if hasattr(s.product, 'quantity'):
                    s.quantity += self.cleaned_data.get('quantity')
                    s.extended_amount += Decimal(self.cleaned_data.get('quantity') * product.price)
                else:
                    s.quantity += 1
                duplicate = True
                s.save()
                break
            else:
                duplicate = False

        if duplicate == False:
            cartItem = cmod.ShoppingCartItems()
            cartItem.product = product
            cartItem.quantity = self.cleaned_data.get('quantity')
            cartItem.user = user
            if hasattr(product, 'quantity'):
                cartItem.extended_amount = Decimal(self.cleaned_data.get('quantity') * product.price)
            else:
                cartItem.extended_amount = product.price
            cartItem.save()

class CommentForm(FormMixIn, forms.Form):
    form_submit = 'Post Comment'
    form_id = 'comment_form'

    def init(self):
        self.fields['comment'] = forms.CharField(label='', max_length=100, required=True)

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        return self.cleaned_data
    
    def commit(self, product):
        print('COMMIT')
        new_comment = cmod.ProductComment()
        new_comment.comment = self.data.get('comment')
        new_comment.product_id = product.id
        new_comment.user_id = self.request.user.id
        new_comment.save()
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.db import transaction

from utils.help_funcs import recalc_cart
from .models import CartItem, Category, Product, Customer
from .mixins import CartMixin, CategoriesMixin
from .forms import RegistrationForm, LoginForm


class IndexView(CategoriesMixin, CartMixin, View):
    
    def get(self, request, *args, **kwargs):
        context = {}
        products = Product.objects.all().order_by("?")[:4]
        context['products'] = products
        context['categories'] = self.categories
        context['cart'] = self.get_cart()
        return render(request, 'index.html', context)


class RegistrationView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        context = {}
        form = RegistrationForm()
        context['form'] = form
        return render(request, 'registration.html', context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        context = {}
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.email = form.cleaned_data['email']
            new_user.username = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone = form.cleaned_data['phone'],
                address = form.cleaned_data['phone'],
            )
            user = authenticate(
                username=new_user.username, password = form.cleaned_data['password']
            )

            login(request, user)
            return HttpResponseRedirect('/')
        else:
            context['form'] = form
            return render(request, 'registration.html', context)


class LoginView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        context = {}
        form = LoginForm()
        context['form'] = form
        return render(request, 'login.html', context)
    
    @staticmethod
    def post(request, *args, **kwargs):
        context = {}
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(
                email = email, password = password,
            )
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            context['form'] = form
            return render(request, 'login.html', context)
        

class ProductDetailView(DetailView, CategoriesMixin, CartMixin):
    model = Product
    context_object_name = 'product'
    template_name = 'product_detail.html'
    pk_url_kwarg = 'pk'


class CategorytDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'category_detail.html'
    pk_url_kwarg = 'pk'


class CartView(View, CategoriesMixin, CartMixin):
    def get(self, request, *args, **kwargs):
        context = {}
        context['cart'] = self.get_cart()
        context['categories']: self.categories
        return render(request, 'cart.html', context)
    

class AddToCartView(CartMixin, View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        qty = int(request.POST.get('qty', 1))
        p = Product.objects.get(id=product_id)
        cart = self.get_cart()
        if p in [item.product for item in cart.items.all()]:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            cart.add(p, qty)
            recalc_cart(cart)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ChangeQtyInCartView(CartMixin, View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        qty = int(request.POST.get('qty', 1))
        cart_item = CartItem.objects.get(id=item_id)
        cart = self.get_cart()
        if cart_item in [item for item in cart.items.all()]:
            cart.change_item_qty(cart_item, qty)
            recalc_cart(cart)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RemoveFromCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        cart = self.get_cart()
        cart_item = CartItem.objects.get(id=item_id)
        if cart_item in [item for item in cart.items.all()]:
            cart.remove(cart_item)
            recalc_cart(cart)
        return HttpResponseRedirect('/cart/')



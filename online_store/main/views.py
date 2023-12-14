from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.db import transaction

from .models import Product, Customer
from .mixins import CategoriesMixin
from .forms import RegistrationForm, LoginForm


class IndexView(CategoriesMixin, View):
    
    def get(self, request, *args, **kwargs):
        context = {}
        products = Product.objects.all().order_by("?")[:4]
        context['products'] = products
        context['categories'] = self.categories
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




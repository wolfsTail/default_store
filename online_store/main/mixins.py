from typing import Any
from django.http import HttpResponseRedirect
from django.views.generic.base import ContextMixin

from .models import Category, Customer, Cart


class CategoriesMixin(ContextMixin):

    @property
    def categories(self):
        return Category.objects.all()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class UserisAuthenticatedMixin:

    @staticmethod
    def _is_authenticated(request):
        if request.user.is_authenticated:
            return False
        return True
    
    def dispatch(self, request, *args, **kwargs):
        request_full_path = request.get_full_path()
        if 'login' in request_full_path or 'registration' in request_full_path:
            if self._is_authenticated(request):
                if request.META.get('HTTP_REFERER'):
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    return HttpResponseRedirect('/')
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
            if self._is_authenticated(request):
                return super().dispatch(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/login/')



class CartMixin(ContextMixin):
    def get_cart(self):
        if self.request.user.is_authenticated:
            customer = Customer.objects.filter(user=self.request.user).first()
            cart = Cart.objects.filter(in_order=False, owner=customer).first()
            if not customer:
                customer = Customer.objects.create(
                    user = self.request.user
                )
            if not cart:
                cart = Cart.objects.create(owner=customer)
                return cart
            return cart
        return Cart.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.get_cart()
        return context


    

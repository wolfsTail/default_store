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
        if self._is_authenticated(request):
            return HttpResponseRedirect('/login/')
        return super().dispatch(request, *args, **kwargs)


class CartMixin(ContextMixin):
    def get_cart(self):
        if self.request.user.is_authenticated:
            customer = Customer.objects.filter(user=self.request.user).first()
            cart = Cart.objects.filter(in_order=False, owner=customer)
            if not customer:
                customer = Customer.objects.create(
                    user = self.request.user
                )
            if not cart:
                cart = Cart.objects.create(owner=customer)
                return cart
            return cart
        return Cart.objects.none()

    

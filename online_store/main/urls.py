from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path

from .views import IndexView, RegistrationView, LoginView, ProductDetailView,\
                    CategorytDetailView, CartView, AddToCartView, RemoveFromCartView,\
                    ChangeQtyInCartView, MakeOrderView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),    
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('category/<int:pk>/', CategorytDetailView.as_view(), name='category'),
    # registration, autorization
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    # cart's logic
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', RemoveFromCartView.as_view(),\
          name='remove_from_cart'),
    path('change-qty/', ChangeQtyInCartView.as_view(), name='change_qty'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
]


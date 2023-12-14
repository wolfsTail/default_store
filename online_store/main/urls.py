from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path

from .views import IndexView, RegistrationView, LoginView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
]
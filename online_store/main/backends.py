# from typing import Any
# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth import get_user_model
# from django.contrib.auth.base_user import AbstractBaseUser
# from django.db.models import Q
# from django.http.request import HttpRequest


# UserModel = get_user_model()


# class ExtendedUserModelBackend(ModelBackend):
#     def authenticate(self, request: HttpRequest, username: str | None = ..., password: str | None = ..., **kwargs: Any) -> AbstractBaseUser | None:
#         if username is None:
#             username = kwargs.get(UserModel.USERNAME_FIELD, kwargs.get(UserModel.EMAIL_FIELD))
#         if username is None or password is None:
#             return
#         try:
#             user = UserModel._default_manager.get(Q(username__exact=username) | Q(email__iexact=username))
#         except UserModel.DoesNotExist:
#             UserModel().set_password(password)
#         else:
#             if user.check_password(password) and self.user_can_authenticate(user):
#                 return user

from django.contrib.auth.backends import ModelBackend, BaseBackend
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None